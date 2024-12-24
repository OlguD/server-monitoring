# MonitorTools.py
import psutil
from typing import Generator, Optional
import paramiko
import socket
from monitor.Models.MonitorModels import ProcessModel

class MonitorTools:
    def __init__(self, server=None):
        """
        server: ServerConfig instance
        """
        self.server = server
        self.ssh = None
        if server:
            try:
                self.connect()
            except Exception as e:
                print(f"SSH connection failed: {str(e)}")
                # IP ve port'u kontrol et
                print(f"Attempting to connect to: {server.ip}:{server.port}")
                raise

    def connect(self):
        """SSH bağlantısı kur"""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Timeout değerlerini ayarla
            self.ssh.connect(
                hostname=self.server.ip,
                port=int(self.server.port),
                username=self.server.username,
                password=self.server.password,
                timeout=10,  # Bağlantı timeout
                banner_timeout=10  # Banner timeout
            )
        except paramiko.AuthenticationException:
            raise Exception("Authentication failed. Check username and password.")
        except paramiko.SSHException as ssh_exception:
            raise Exception(f"SSH error: {str(ssh_exception)}")
        except socket.timeout:
            raise Exception(f"Timeout connecting to {self.server.ip}:{self.server.port}")
        except Exception as e:
            raise Exception(f"Connection failed: {str(e)}")

    def execute_command(self, command):
        """SSH üzerinden komut çalıştır"""
        if not self.ssh:
            raise Exception("No SSH connection")
        
        stdin, stdout, stderr = self.ssh.exec_command(command)
        error = stderr.read().decode()
        if error:
            raise Exception(f"Command error: {error}")
        return stdout.read().decode()

    def cpu_usage(self):
        """CPU kullanımını al"""
        if not self.server:
            return psutil.cpu_percent(interval=0.1)
        
        try:
            # Linux top komutu ile CPU kullanımını al
            command = "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'"
            result = self.execute_command(command)
            return float(result)
        except Exception as e:
            print(f"CPU usage error: {e}")
            return 0.0

    def memory_usage(self):
        """Bellek kullanımını al"""
        if not self.server:
            return psutil.virtual_memory().percent
        
        try:
            # Free komutu ile bellek kullanımını al
            command = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
            result = self.execute_command(command)
            return float(result)
        except Exception as e:
            print(f"Memory usage error: {e}")
            return 0.0

    def disk_usage(self):
        """Disk kullanımını al"""
        if not self.server:
            return psutil.disk_usage('/').percent
        
        try:
            # Df komutu ile disk kullanımını al
            command = "df / | tail -1 | awk '{print $5}' | sed 's/%//'"
            result = self.execute_command(command)
            return float(result)
        except Exception as e:
            print(f"Disk usage error: {e}")
            return 0.0

    def network_usage(self):
        """Ağ kullanımını al"""
        if not self.server:
            network = psutil.net_io_counters()
            network_usage = network.bytes_sent + network.bytes_recv
            bytes_sent = network.bytes_sent
            bytes_recv = network.bytes_recv
            network_usage_gb = round(network_usage / (1024 * 1024 * 1024), 2)
            sent_mb = round(bytes_sent / (1024 * 1024), 2)
            recv_mb = round(bytes_recv / (1024 * 1024), 2)
            return network_usage_gb, sent_mb, recv_mb
        
        try:
            # İlk ölçümü al
            command1 = "cat /proc/net/dev | grep eth0 | awk '{print $2,$10}'"
            result1 = self.execute_command(command1)
            recv1, sent1 = map(int, result1.split())
            
            # 1 saniye bekle
            import time
            time.sleep(1)
            
            # İkinci ölçümü al
            command2 = "cat /proc/net/dev | grep eth0 | awk '{print $2,$10}'"
            result2 = self.execute_command(command2)
            recv2, sent2 = map(int, result2.split())
            
            # Farkları hesapla
            recv_rate = (recv2 - recv1) / 1024 / 1024  # MB/s
            sent_rate = (sent2 - sent1) / 1024 / 1024  # MB/s
            total_rate = (recv_rate + sent_rate) / 1024  # GB/s
            
            return total_rate, sent_rate, recv_rate
        except Exception as e:
            print(f"Network usage error: {e}")
            return 0.0, 0.0, 0.0

    def get_process_details(
        self,
        top_n: Optional[int] = 10,
        min_cpu: float = 0.05,
        min_memory: float = 0.05
    ) -> Generator[ProcessModel, None, None]:
        """
        Get process details from the system.
        
        Args:
            top_n: Number of top processes to return
            min_cpu: Minimum CPU percentage threshold
            min_memory: Minimum memory percentage threshold
            
        Returns:
            Generator yielding ProcessModel instances for matching processes
        """
        if not self.server:
            return super().get_process_details(top_n, min_cpu, min_memory)
        
        try:
            # Explicitly skip the header row using awk to start from line 2
            command = f"ps aux | awk 'NR>1' | sort -rn -k3 | head -n {top_n}"
            result = self.execute_command(command)
            
            for line in result.splitlines():
                try:
                    # Split the line while preserving the command
                    parts = line.split(None, 10)
                    if len(parts) < 11:
                        continue
                    
                    # Parse process information
                    pid = int(parts[1])
                    cpu_percent = float(parts[2])
                    memory_percent = float(parts[3])
                    memory_rss = float(parts[5])  # RSS in KB
                    memory_mb = memory_rss / 1024  # Convert KB to MB
                    command_name = parts[10]
                    
                    # Only yield processes that meet the threshold requirements
                    if cpu_percent >= min_cpu and memory_percent >= min_memory:
                        process = ProcessModel(
                            pid=pid,
                            name=command_name,
                            cpu_percent=cpu_percent,
                            memory_percent=memory_percent,
                            memory_usage=memory_mb,
                            status='running'
                        )
                        yield process
                        
                except (ValueError, IndexError) as e:
                    # Skip lines that can't be parsed instead of printing errors
                    continue
                
        except Exception as e:
            print(f"Process detail error: {e}")
            return iter([])

    def __del__(self):
        """Bağlantıyı kapat"""
        if self.ssh:
            self.ssh.close()