document.addEventListener('DOMContentLoaded', function () {
    const purchaseData = JSON.parse(localStorage.getItem('purchaseData')) || [];
    const ctx = document.getElementById('purchaseChartCanvas')?.getContext('2d');

    if (purchaseData.length > 0) {
        // Mostrar gráfico y botones si hay datos
        document.getElementById('chartContainer').style.display = 'block';
        document.getElementById('noDataMessage').style.display = 'none';
        document.getElementById('buttonsContainer').style.display = 'block';

        // Extraer fechas y datos
        const labels = purchaseData.map(item => `${item.date} - ${item.description}`);
        const data = purchaseData.map(item => parseFloat(item.price.replace(/[^0-9.-]+/g, "") / 100) * item.quantity);

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Gastado por Producto',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
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
                            label: function(tooltipItem) {
                                const label = tooltipItem.label || '';
                                const value = tooltipItem.raw;
                                return `${label}: $${value.toFixed(2)}`;
                            },
                            title: function(tooltipItem) {
                                const item = tooltipItem[0];
                                const date = purchaseData[item.dataIndex].date;
                                return `Fecha: ${date}`;
                            }
                        }
                    }
                },
                layout: {
                    padding: 10
                }
            }
        });

        // Función para limpiar los datos del gráfico y eliminar de localStorage
        document.getElementById('clearChartButton').addEventListener('click', function () {
            // Limpiar datos del gráfico
            chart.data.labels = [];
            chart.data.datasets.forEach((dataset) => {
                dataset.data = [];
            });
            chart.update();

            // Eliminar datos de localStorage
            localStorage.removeItem('purchaseData');

            // Mostrar mensaje de no hay datos
            document.getElementById('chartContainer').style.display = 'none';
            document.getElementById('noDataMessage').style.display = 'block';
            document.getElementById('buttonsContainer').style.display = 'none';
        });

        // Función para generar el PDF con tabla
        document.getElementById('generatePdfButton').addEventListener('click', function () {
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF();

            if (purchaseData.length === 0) {
                pdf.text("No hay estadísticas que mostrar.", 14, 10);
                pdf.save('factura.pdf');
                return;
            }

            // Crear tabla en PDF
            const tableData = purchaseData.map(item => [
                item.date,
                item.description,
                item.price,
                item.quantity,
                (parseFloat(item.price.replace(/[^0-9.-]+/g, "") / 100) * item.quantity).toFixed(2)
            ]);

            const tableHeaders = ['Fecha', 'Descripción', 'Precio', 'Cantidad', 'Total'];

            // Calcular total general
            const totalAmount = tableData.reduce((acc, row) => acc + parseFloat(row[4]), 0).toFixed(2);

            // Agregar fila con total
            tableData.push(['', '', '', 'Total', `$${totalAmount}`]);

            pdf.text("Estadísticas de Compra", 14, 10);
            pdf.autoTable({
                head: [tableHeaders],
                body: tableData,
                startY: 20,
                theme: 'grid'
            });

            pdf.save('factura.pdf');
        });
    } else {
        // Ocultar gráfico y botones, mostrar mensaje de no hay datos
        document.getElementById('chartContainer').style.display = 'none';
        document.getElementById('noDataMessage').style.display = 'block';
        document.getElementById('buttonsContainer').style.display = 'none';
    }
});
