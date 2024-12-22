from monitor.utils.MonitorTools import MonitorTools
from django.test import TestCase


class TestMonitor(TestCase):
    def test_cpu_usage(self):
        cpu_usage = MonitorTools.cpu_usage()
        self.assertIsInstance(cpu_usage, float)
        self.assertGreaterEqual(cpu_usage, 0)
        self.assertLessEqual(cpu_usage, 100)

    def test_memory_usage(self):
        memory_usage = MonitorTools.memory_usage()
        self.assertIsInstance(memory_usage, float)
        self.assertGreaterEqual(memory_usage, 0)
        self.assertLessEqual(memory_usage, 100)

    def test_disk_usage(self):
        disk_usage = MonitorTools.disk_usage()
        self.assertIsInstance(disk_usage, float)
        self.assertGreaterEqual(disk_usage, 0)
        self.assertLessEqual(disk_usage, 100)

    def test_network_usage(self):
        network_usage, sent_mb, recv_mb = MonitorTools.network_usage()
        self.assertIsInstance(network_usage, float)
        self.assertIsInstance(sent_mb, float)
        self.assertIsInstance(recv_mb, float)
        self.assertGreaterEqual(network_usage, 0)
        self.assertGreaterEqual(sent_mb, 0)
        self.assertGreaterEqual(recv_mb, 0)

    def test_get_process_details(self):
        process_details = MonitorTools.get_process_details()
        for process in process_details:
            self.assertIsInstance(process.pid, int)
            self.assertIsInstance(process.name, str)
            self.assertIsInstance(process.cpu_percent, float)
            self.assertIsInstance(process.memory_percent, float)
            self.assertIsInstance(process.memory_usage, float)
            self.assertIsInstance(process.status, str)
            self.assertGreaterEqual(process.pid, 0)
            self.assertGreaterEqual(process.cpu_percent, 0)
            self.assertGreaterEqual(process.memory_percent, 0)
            self.assertGreaterEqual(process.memory_usage, 0)
    
if "__main__" == __name__:
    unittest.main()