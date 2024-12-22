from django.test import TestCase
from unittest.mock import patch, Mock
from monitor.utils.ContinuousMonitor import ContinuousMonitor
from monitor.Models.MonitorModels import (AllMonitorModel, CPUModel, 
                                        MemoryModel, DiskModel, NetworkModel)
import time
import psutil
import gc


class TestContinuousMonitor(TestCase):
    def setUp(self):
        self.monitor = ContinuousMonitor(interval=1)
        
    def tearDown(self):
        if self.monitor:
            self.monitor.stop_monitoring()

    def test_monitor_initialization(self):
        """Test monitor initialization"""
        self.assertIsNone(self.monitor.shared_data)
        self.assertEqual(self.monitor.interval, 1)
        self.assertIsNotNone(self.monitor.lock)
        self.assertIsNotNone(self.monitor.stop_event)
        self.assertIsNone(self.monitor.thread)

    @patch('monitor.utils.MonitorTools.MonitorTools.cpu_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.memory_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.disk_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.network_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.get_process_details')
    def test_data_collection(self, mock_processes, mock_network, mock_disk, 
                           mock_memory, mock_cpu):
        """Test if monitor collects and stores data correctly"""
        # Mock return values
        mock_cpu.return_value = 50.0
        mock_memory.return_value = 60.0
        mock_disk.return_value = 70.0
        mock_network.return_value = (80.0, 90.0, 100.0)
        mock_processes.return_value = []

        # Start monitoring
        self.monitor.start_monitoring()
        
        # Wait for data collection
        time.sleep(2)
        
        # Get collected data
        data = self.monitor.get_data()
        
        # Verify data
        self.assertIsNotNone(data)
        self.assertIsInstance(data, AllMonitorModel)
        self.assertEqual(data.cpu.usage, 50.0)
        self.assertEqual(data.memory.usage, 60.0)
        self.assertEqual(data.disk.usage, 70.0)
        self.assertEqual(data.network.total_usage_gb, 80.0)
        self.assertEqual(data.network.sent_mb, 90.0)
        self.assertEqual(data.network.recv_mb, 100.0)
        self.assertEqual(len(data.processes), 0)

        # Stop monitoring
        self.monitor.stop_monitoring()

    def test_start_and_stop_monitoring(self):
        """Test starting and stopping monitoring"""
        self.monitor.start_monitoring()
        time.sleep(0.1)
        self.assertIsNotNone(self.monitor.thread)
        self.assertTrue(self.monitor.thread.is_alive())
        
        self.monitor.stop_monitoring()
        self.assertFalse(self.monitor.thread.is_alive())

    @patch('monitor.utils.MonitorTools.MonitorTools.cpu_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.memory_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.disk_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.network_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.get_process_details')
    def test_thread_safety(self, mock_processes, mock_network, mock_disk, 
                          mock_memory, mock_cpu):
        """Test thread safety of data access"""
        # Mock return values
        mock_cpu.return_value = 50.0
        mock_memory.return_value = 60.0
        mock_disk.return_value = 70.0
        mock_network.return_value = (80.0, 90.0, 100.0)
        mock_processes.return_value = []

        self.monitor.start_monitoring()
        
        results = []
        for _ in range(5):
            data = self.monitor.get_data()
            if data and hasattr(data, 'cpu'):
                results.append(data.cpu.usage)
            time.sleep(0.1)
        
        self.monitor.stop_monitoring()
        
        # Verify all readings are consistent
        if results:
            self.assertTrue(all(x == 50.0 for x in results))

    def test_invalid_interval(self):
        """Test monitor with invalid interval"""
        with self.assertRaises(ValueError):
            ContinuousMonitor(interval=-1)

    @patch('monitor.utils.MonitorTools.MonitorTools.cpu_usage')
    def test_error_handling(self, mock_cpu):
        """Test error handling during monitoring"""
        # Mock CPU usage to raise an exception
        mock_cpu.side_effect = Exception("Test error")
        
        self.monitor.start_monitoring()
        time.sleep(0.1)
        
        # Thread should still be alive despite the error
        self.assertTrue(self.monitor.thread.is_alive())
        
        # Data should be None or last valid data
        data = self.monitor.get_data()
        self.assertIsNone(data)
        
        self.monitor.stop_monitoring()

    def test_memory_leak(self):
        """Test memory leak by monitoring memory usage during extended operation"""
        # İlk bellek kullanımını kaydet
        gc.collect()  # Garbage collection'ı zorla
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB cinsinden

        # Monitörü başlat ve bir süre çalıştır
        self.monitor.start_monitoring()
        
        memory_samples = []
        # 10 örnek al, her biri 1 saniye arayla
        for _ in range(10):
            gc.collect()
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory)
            time.sleep(1)

        self.monitor.stop_monitoring()

        # Son bellek kullanımını al
        gc.collect()
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024

        # Bellek artışının makul sınırlar içinde olduğunu kontrol et
        # Genellikle 10MB'dan fazla artış olmamalı
        memory_increase = final_memory - initial_memory
        self.assertLess(memory_increase, 10.0, 
                       f"Memory increased by {memory_increase:.2f}MB, which exceeds the threshold")

        # Bellek kullanımının kararlı olduğunu kontrol et
        # Son 5 örneğin standart sapmasını hesapla
        last_samples = memory_samples[-5:]
        mean = sum(last_samples) / len(last_samples)
        variance = sum((x - mean) ** 2 for x in last_samples) / len(last_samples)
        std_dev = variance ** 0.5

        # Standart sapma 1MB'dan az olmalı
        self.assertLess(std_dev, 1.0, 
                       f"Memory usage is unstable. Standard deviation: {std_dev:.2f}MB")


    @patch('monitor.utils.MonitorTools.MonitorTools.cpu_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.memory_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.disk_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.network_usage')
    @patch('monitor.utils.MonitorTools.MonitorTools.get_process_details')
    def test_load(self, mock_processes, mock_network, mock_disk, 
                 mock_memory, mock_cpu):
        """Test system under high load with rapid data requests"""
        # Mock değerlerini ayarla
        mock_cpu.return_value = 50.0
        mock_memory.return_value = 60.0
        mock_disk.return_value = 70.0
        mock_network.return_value = (80.0, 90.0, 100.0)
        mock_processes.return_value = []

        # Monitörü başlat
        self.monitor.start_monitoring()
        time.sleep(0.1)  # Başlaması için bekle

        try:
            # Hızlı ve yoğun veri istekleri simülasyonu
            start_time = time.time()
            request_count = 0
            successful_requests = 0
            failed_requests = 0

            # 5 saniye boyunca sürekli veri iste
            while time.time() - start_time < 5:
                try:
                    data = self.monitor.get_data()
                    if data is not None:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                    request_count += 1
                    time.sleep(0.01)  # Çok küçük bir bekleme
                except Exception as e:
                    failed_requests += 1
                    print(f"Error during load test: {e}")

            # Sonuçları değerlendir
            total_time = time.time() - start_time
            requests_per_second = request_count / total_time
            success_rate = (successful_requests / request_count) * 100 if request_count > 0 else 0

            # Testleri kontrol et
            self.assertGreater(requests_per_second, 50,  # Saniyede en az 50 istek
                             f"Request rate too low: {requests_per_second:.2f} req/s")
            self.assertGreater(success_rate, 95,  # En az %95 başarı oranı
                             f"Success rate too low: {success_rate:.2f}%")
            self.assertLess(failed_requests, request_count * 0.05,  # En fazla %5 hata
                          f"Too many failed requests: {failed_requests}")

            print(f"\nLoad Test Results:")
            print(f"Total Requests: {request_count}")
            print(f"Successful Requests: {successful_requests}")
            print(f"Failed Requests: {failed_requests}")
            print(f"Requests per second: {requests_per_second:.2f}")
            print(f"Success Rate: {success_rate:.2f}%")

        finally:
            self.monitor.stop_monitoring()

    def test_concurrent_start_stop(self):
        """Test rapid start/stop operations"""
        for _ in range(10):  # 10 kez hızlı başlat/durdur
            self.monitor.start_monitoring()
            time.sleep(0.1)
            self.monitor.stop_monitoring()
            time.sleep(0.1)


if __name__ == '__main__':
    unittest.main()