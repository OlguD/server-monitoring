import  ChartManager  from './charts.js';

const DashboardMonitor = {
    interval: null,
    isMonitoring: false,

    getSelectedServer() {
        const serverSelect = document.querySelector('select[name="servers"]');
        return serverSelect ? serverSelect.value : null;
    },

    updateDashboard() {
        const selectedServer = this.getSelectedServer();
        
        if (!selectedServer) {
            console.log('No server selected, skipping update');
            return;
        }

        fetch(`/dashboard/dashboard-data/?server=${encodeURIComponent(selectedServer)}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(async response => {
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Raw API Response:', data);
            this.updateMetrics(data);
            // ChartManager'ı da aynı veriyle güncelle
            ChartManager.updateChart(data);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            this.stopMonitoring();
        });
    },

    updateMetrics(data) {
        const formatValue = (value) => {
            const num = Number(value || 0);
            return num < 1 ? num.toFixed(3) : num.toFixed(1);
        };

        // CPU Usage güncelleme
        const cpuValueElement = document.getElementById('cpu-usage-value');
        const cpuBarElement = document.getElementById('cpu-usage-bar');
        
        if (cpuValueElement && cpuBarElement) {
            const cpuUsage = Number(data.cpu?.usage || 0);
            cpuValueElement.textContent = `${formatValue(cpuUsage)} %`;
            cpuBarElement.style.width = `${Math.max(cpuUsage, 0.5)}%`;
        }

        // Memory Usage güncelleme
        const memoryValueElement = document.getElementById('memory-usage-value');
        const memoryBarElement = document.getElementById('memory-usage-bar');
        
        if (memoryValueElement && memoryBarElement) {
            const memUsage = Number(data.memory?.usage || 0);
            memoryValueElement.textContent = `${formatValue(memUsage)} %`;
            memoryBarElement.style.width = `${Math.max(memUsage, 0.5)}%`;
        }

        // Disk Usage güncelleme
        const diskValueElement = document.getElementById('disk-usage-value');
        const diskBarElement = document.getElementById('disk-usage-bar');
        
        if (diskValueElement && diskBarElement) {
            const diskUsage = Number(data.disk?.usage || 0);
            diskValueElement.textContent = `${formatValue(diskUsage)} %`;
            diskBarElement.style.width = `${Math.max(diskUsage, 0.5)}%`;
        }

        // Network Usage güncelleme
        const networkValueElement = document.getElementById('network-usage-value');
        if (networkValueElement) {
            const totalUsage = Number(data.network?.total_usage_gb || 0);
            if (totalUsage < 1) {
                const mbValue = totalUsage * 1000;
                networkValueElement.textContent = `${mbValue.toFixed(3)} MB/s`;
            } else {
                networkValueElement.textContent = `${totalUsage.toFixed(3)} GB/s`;
            }
        }
    },

    startMonitoring() {
        const selectedServer = this.getSelectedServer();
        if (!selectedServer) {
            alert('Please select a server first');
            return;
        }

        if (!this.interval) {
            this.updateDashboard();  // İlk veriyi al
            this.interval = setInterval(() => this.updateDashboard(), 5000);
        }
    },

    stopMonitoring() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
};

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('monitoringToggle');
    const playIcon = document.getElementById('playIcon');
    const stopIcon = document.getElementById('stopIcon');
    const toggleText = document.getElementById('toggleText');
    const serverSelect = document.querySelector('select[name="servers"]');
    const countdownElement = document.getElementById('countdown');

    // Chart'ı başlat
    ChartManager.init();

    if (countdownElement) {
        CountdownManager.start(countdownElement);
    }

    // İzlemeyi durdur
    DashboardMonitor.stopMonitoring();

    serverSelect?.addEventListener('change', function() {
        if (DashboardMonitor.isMonitoring) {
            DashboardMonitor.stopMonitoring();
            DashboardMonitor.isMonitoring = false;
            toggleButton.classList.remove('bg-red-500', 'hover:bg-red-600');
            toggleButton.classList.add('bg-blue-500', 'hover:bg-blue-600');
            playIcon.classList.remove('hidden');
            stopIcon.classList.add('hidden');
            toggleText.textContent = 'Start Monitoring';
        }
    });

    toggleButton?.addEventListener('click', function() {
        const selectedServer = DashboardMonitor.getSelectedServer();
        if (!selectedServer) {
            alert('Please select a server first');
            return;
        }

        DashboardMonitor.isMonitoring = !DashboardMonitor.isMonitoring;
        
        if (DashboardMonitor.isMonitoring) {
            DashboardMonitor.startMonitoring();
            toggleButton.classList.remove('bg-blue-500', 'hover:bg-blue-600');
            toggleButton.classList.add('bg-red-500', 'hover:bg-red-600');
            playIcon.classList.add('hidden');
            stopIcon.classList.remove('hidden');
            toggleText.textContent = 'Stop Monitoring';
        } else {
            DashboardMonitor.stopMonitoring();
            toggleButton.classList.remove('bg-red-500', 'hover:bg-red-600');
            toggleButton.classList.add('bg-blue-500', 'hover:bg-blue-600');
            playIcon.classList.remove('hidden');
            stopIcon.classList.add('hidden');
            toggleText.textContent = 'Start Monitoring';
        }
    });
});