import psutil
from typing import Generator, Optional
from monitor.Models.MonitorModels import ProcessModel

class MonitorTools:
    @staticmethod
    def cpu_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        return cpu_usage

    @staticmethod
    def memory_usage():
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        return memory_usage

    @staticmethod
    def disk_usage():
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        return disk_usage

    @staticmethod
    def network_usage():
        network = psutil.net_io_counters()
        network_usage = network.bytes_sent + network.bytes_recv
        bytes_sent = network.bytes_sent
        bytes_recv = network.bytes_recv
        network_usage_gb = round(network_usage / (1024 * 1024 * 1024), 2)
        sent_mb = round(bytes_sent / (1024 * 1024), 2)
        recv_mb = round(bytes_recv / (1024 * 1024), 2)

        return network_usage_gb, sent_mb, recv_mb

    @staticmethod
    def get_process_details(
        top_n: Optional[int] = 10,  # Varsayılan olarak top 10 process
        min_cpu: float = 0.05,        # En az %0.05 CPU kullanan processler
        min_memory: float = 0.05      # En az %0.05 bellek kullanan processler
    ) -> Generator[ProcessModel, None, None]:
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    process = psutil.Process(proc.pid)
                    
                    cpu_percent = process.cpu_percent()
                    memory_percent = process.memory_percent()
                    
                    # Filtreleme kriterleri
                    if (cpu_percent >= min_cpu and 
                        memory_percent >= min_memory):
                        
                        process_info = ProcessModel(
                            pid=proc.pid,
                            name=proc.info['name'],
                            cpu_percent=cpu_percent,
                            memory_percent=memory_percent,
                            memory_usage=process.memory_info().rss / (1024 * 1024),
                            status=proc.info['status']
                        )
                        
                        processes.append(process_info)
                        
                        # Eğer top_n belirtildiyse sınırla
                        if top_n and len(processes) >= top_n:
                            break
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # CPU kullanımına göre sıralama
            return sorted(processes, key=lambda x: x.cpu_percent, reverse=True)
        
        except Exception as e:
            print(f"Process detail error: {e}")
            return []