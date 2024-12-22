// dashboard.js

let monitoringInterval = null;
let isMonitoring = false;

function getSelectedServer() {
    const serverSelect = document.querySelector('select[name="servers"]');
    const selectedServer = serverSelect ? serverSelect.value : null;
    return selectedServer;
}

function updateDashboard() {
    const selectedServer = getSelectedServer();
    
    if (!selectedServer) {
        console.log('No server selected, skipping update');
        return;
    }

    console.log("Fetching data for server:", selectedServer);
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
        
        // Hassas formatlamak için yardımcı fonksiyon
        const formatValue = (value) => {
            const num = Number(value || 0);
            // Değer 1'den küçükse 3 ondalık, değilse 1 ondalık göster
            return num < 1 ? num.toFixed(3) : num.toFixed(1);
        };
        
        // CPU Usage güncelleme
        const cpuValueElement = document.getElementById('cpu-usage-value');
        const cpuBarElement = document.getElementById('cpu-usage-bar');
        
        if (cpuValueElement && cpuBarElement) {
            const cpuUsage = Number(data.cpu?.usage || 0);
            cpuValueElement.textContent = `${formatValue(cpuUsage)} %`;
            // Progress bar için minimum 0.5% genişlik kullan ki çok küçük değerler de görünsün
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
            // Network için daha hassas format
            if (totalUsage < 0.001) {
                const mbValue = totalUsage * 1000;
                networkValueElement.textContent = `${mbValue.toFixed(3)} MB`;
            } else {
                networkValueElement.textContent = `${totalUsage.toFixed(3)} GB`;
            }
        }
    })
    .catch(error => {
        console.error('Error fetching dashboard data:', error);
        stopMonitoring();
    });
}

function startMonitoring() {
    const selectedServer = getSelectedServer();
    if (!selectedServer) {
        alert('Please select a server first');
        return;
    }

    if (!monitoringInterval) {
        updateDashboard(); // İlk güncelleme
        monitoringInterval = setInterval(updateDashboard, 5000);
    }
}

function stopMonitoring() {
    if (monitoringInterval) {
        clearInterval(monitoringInterval);
        monitoringInterval = null;
    }
}

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('monitoringToggle');
    const playIcon = document.getElementById('playIcon');
    const stopIcon = document.getElementById('stopIcon');
    const toggleText = document.getElementById('toggleText');
    const serverSelect = document.querySelector('select[name="servers"]');

    // İlk yüklemede güncelleme yapma
    stopMonitoring();

    // Server seçimi değiştiğinde monitoring'i durdur
    serverSelect.addEventListener('change', function() {
        if (isMonitoring) {
            stopMonitoring();
            isMonitoring = false;
            toggleButton.classList.remove('bg-red-500', 'hover:bg-red-600');
            toggleButton.classList.add('bg-blue-500', 'hover:bg-blue-600');
            playIcon.classList.remove('hidden');
            stopIcon.classList.add('hidden');
            toggleText.textContent = 'Start Monitoring';
        }
    });

    toggleButton.addEventListener('click', function() {
        const selectedServer = getSelectedServer();
        if (!selectedServer) {
            alert('Please select a server first');
            return;
        }

        isMonitoring = !isMonitoring;
        
        if (isMonitoring) {
            startMonitoring();
            toggleButton.classList.remove('bg-blue-500', 'hover:bg-blue-600');
            toggleButton.classList.add('bg-red-500', 'hover:bg-red-600');
            playIcon.classList.add('hidden');
            stopIcon.classList.remove('hidden');
            toggleText.textContent = 'Stop Monitoring';
        } else {
            stopMonitoring();
            toggleButton.classList.remove('bg-red-500', 'hover:bg-red-600');
            toggleButton.classList.add('bg-blue-500', 'hover:bg-blue-600');
            playIcon.classList.remove('hidden');
            stopIcon.classList.add('hidden');
            toggleText.textContent = 'Start Monitoring';
        }
    });
});