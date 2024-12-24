const ChartManager = {
    chart: null,
    ctx: document.getElementById('chart'),

    init() {
        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: Array.from({ length: 10 }, () => ''),
                datasets: [
                    {
                        label: 'CPU Usage',
                        data: Array.from({ length: 10 }, () => 0),
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2,
                        fill: false,
                        pointRadius: 0,
                    },
                    {
                        label: 'Memory Usage',
                        data: Array.from({ length: 10 }, () => 0),
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        fill: false,
                        pointRadius: 0,
                    },
                    {
                        label: 'Disk Usage',
                        data: Array.from({ length: 10 }, () => 0),
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false,
                        pointRadius: 0,
                    },
                ],
            },
            options: {
                responsive: true,
                animation: true,
                scales: {
                    x: {
                        display: true,
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            display: true
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    },

    updateChart(data) {
        if (!this.chart) return;

        const time = new Date().toLocaleTimeString();
        
        this.chart.data.labels.shift();
        this.chart.data.labels.push(time);

        const cpuUsage = Number(data.cpu?.usage || 0);
        const memUsage = Number(data.memory?.usage || 0);
        const diskUsage = Number(data.disk?.usage || 0);
        
        this.chart.data.datasets[0].data.shift();
        this.chart.data.datasets[0].data.push(cpuUsage);
        
        this.chart.data.datasets[1].data.shift();
        this.chart.data.datasets[1].data.push(memUsage);
        
        this.chart.data.datasets[2].data.shift();
        this.chart.data.datasets[2].data.push(diskUsage);
        
        this.chart.update();
    },

    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
};

export default ChartManager;