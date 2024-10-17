document.addEventListener('DOMContentLoaded', function () {
    const purchaseData = JSON.parse(localStorage.getItem('purchaseData')) || [];

    if (purchaseData.length > 0) {
        // Mostrar gráfico y botones si hay datos
        document.getElementById('noDataMessage').style.display = 'none';
        document.getElementById('buttonsContainer').style.display = 'block';

        // Extraer fechas y datos
        const categories = purchaseData.map(item => `${item.date} - ${item.description}`);
        const data = purchaseData.map(item => parseFloat(item.price.replace(/[^0-9.-]+/g, "")/100) * item.quantity);

        var optionsLine = {
            series: [{
                name: 'Total Gastado por Producto',
                data: data
            }],
            chart: {
                height: 500,
                type: 'line',
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },

            grid: {
                row: {
                    colors: ['#f3f3f3', 'transparent'],
                    opacity: 0.5
                },
            },
            xaxis: {
                categories: categories,
                title: {
                    text: 'Fecha - Descripción'
                }
            },
            yaxis: {
                title: {
                    text: 'Total ($)'
                }
            },
            colors: ['#1E3A8A'],
        };

        var lineChart = new ApexCharts(document.querySelector("#purchaseChart"), optionsLine);
        lineChart.render();

        // Función para limpiar los datos del gráfico y eliminar de localStorage
        document.getElementById('clearChartButton').addEventListener('click', function () {
            // Limpiar datos del gráfico
            lineChart.updateSeries([{ data: [] }]);

            // Eliminar datos de localStorage
            localStorage.removeItem('purchaseData');

            // Mostrar mensaje de no hay datos
            document.getElementById('noDataMessage').style.display = 'block';
            document.getElementById('buttonsContainer').style.display = 'none';
        });

        // Función para descargar el gráfico como imagen
        document.getElementById('downloadChartButton').addEventListener('click', function () {
            lineChart.exportMenu.exportToSVG();
        });

    } else {
        // Ocultar gráfico y botones, mostrar mensaje de no hay datos
        document.getElementById('noDataMessage').style.display = 'block';
        document.getElementById('buttonsContainer').style.display = 'none';
    }
});
