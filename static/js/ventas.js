document.addEventListener('DOMContentLoaded', function () {
    let barChart = null; // Variable para almacenar la instancia del gráfico de barras
    let pieChart = null; // Variable para almacenar la instancia del gráfico de pastel

    // Función para obtener datos y actualizar los gráficos
    function fetchAndUpdateCharts(startDate, endDate) {
        let url = '/sales/estadisticas_venta/';
        
        // Construye la URL con las fechas proporcionadas si están disponibles
        if (startDate && endDate) {
            url += `?start_date=${startDate}&end_date=${endDate}`;
        }
        console.log(`URL construida: ${url}`);

        // Realiza la solicitud de datos al servidor
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            console.log('Respuesta recibida:', response);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            if (!data || data.length === 0) {
                document.getElementById('noDataMessage').style.display = 'block';
                if (barChart) {
                    barChart.destroy();
                }
                if (pieChart) {
                    pieChart.destroy();
                }
                return;
            }
            document.getElementById('noDataMessage').style.display = 'none';

            // Procesar los datos
            const processedBarData = processBarData(data);
            const processedPieData = processPieData(data);

            // Crear o actualizar los gráficos
            createOrUpdateBarChart(processedBarData);
            createOrUpdatePieChart(processedPieData);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Hubo un error al obtener los datos. Por favor, intenta de nuevo.');
        });
    }

    // Función para procesar los datos para el gráfico de barras
    function processBarData(data) {
        const dateMap = new Map();
    
        data.forEach(item => {
            const date = new Date(item.issue_date).toLocaleDateString();
            
            if (dateMap.has(date)) {
                dateMap.set(date, dateMap.get(date) + 1);
            } else {
                dateMap.set(date, 1);
            }
        });
    
        return {
            labels: Array.from(dateMap.keys()),
            data: Array.from(dateMap.values())
        };
    }

    // Función para procesar los datos para el gráfico de pastel
    function processPieData(data) {
        const dateMap = new Map();
    
        data.forEach(item => {
            const date = new Date(item.issue_date).toLocaleDateString();
            
            if (dateMap.has(date)) {
                dateMap.set(date, dateMap.get(date) + item.total_sales);
            } else {
                dateMap.set(date, item.total_sales);
            }
        });
    
        return {
            labels: Array.from(dateMap.keys()),
            data: Array.from(dateMap.values())
        };
    }

    // Función para crear o actualizar el gráfico de barras
    function createOrUpdateBarChart(processedData) {
        const ctx = document.getElementById('columnvent').getContext('2d');
    
        if (barChart) {
            barChart.destroy();
        }
    
        barChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: processedData.labels,
                datasets: [{
                    label: 'Número de Facturas por Día',
                    data: processedData.data,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Facturas: ${context.parsed.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Fecha'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Número de Facturas'
                        },
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    // Función para crear o actualizar el gráfico de pastel
    function createOrUpdatePieChart(processedData) {
        const ctx = document.getElementById('pieChart').getContext('2d');

        if (pieChart) {
            pieChart.destroy();
        }

        pieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: processedData.labels,
                datasets: [{
                    label: 'Total de Ventas por Día',
                    data: processedData.data,
                    backgroundColor: processedData.labels.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.2)`),
                    borderColor: processedData.labels.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 1)`),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(2);
                                return `${label}: $${value.toFixed(2)} (${percentage}%)`;
                            }
                        }
                    },
                    datalabels: {
                        display: true,
                        formatter: function(value, context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(2);
                            return `${percentage}%`;
                        },
                        color: '#000',
                        font: {
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    }

    // Añade un listener al botón para actualizar los gráficos
    document.querySelector('button[onclick="updateCharts()"]').addEventListener('click', function () {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;

        console.log(`Fecha de inicio: ${startDate}, Fecha de fin: ${endDate}`);

        if (startDate && endDate) {
            fetchAndUpdateCharts(startDate, endDate);
        } else {
            alert('Por favor, selecciona un rango de fechas.');
        }
    });

    // Llama a fetchAndUpdateCharts sin fechas para cargar los datos iniciales
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    fetchAndUpdateCharts(startDate, endDate);
});
