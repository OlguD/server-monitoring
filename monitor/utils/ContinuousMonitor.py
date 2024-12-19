import threading
import time
from monitor.utils import MonitorTools
from monitor.Models.MonitorModels import (AllMonitorModel,
                  CPUModel, MemoryModel,
                  DiskModel, NetworkModel)

class ContinuousMonitor:
    def __init__(self, interval=30):
        self.lock = threading.Lock()
        self.shared_data = None
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = None


    def start_monitoring(self):
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.deamon = True
        self.thread.start()

    def stop_monitoring(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()

    def _monitor_loop(self):
        while not self.stop_event.is_set():
            # self.cpu_usage = MonitorTools.cpu_usage()
            # self.memory_usage = MonitorTools.memory_usage()
            # self.disk_usage = MonitorTools.disk_usage()
            # self.network_usage = MonitorTools.network_usage()
            # self.processes = list(MonitorTools.get_process_details())

            all_monitor = AllMonitorModel(
                cpu=CPUModel(usage=MonitorTools.cpu_usage()),
                memory=MemoryModel(usage=MonitorTools.memory_usage()),
                disk=DiskModel(usage=MonitorTools.disk_usage()),
                network=NetworkModel(
                    total_usage_gb=network_data[0],
                    sent_mb=network_data[1],
                    recv_mb=network_data[2]
                ),
                processes=list(MonitorTools.get_process_details())
            )

            with self.lock:
                self.shared_data = all_monitor

            time.sleep(self.interval)

    def get_data(self):
        with self.lock:
            return self.shared_data