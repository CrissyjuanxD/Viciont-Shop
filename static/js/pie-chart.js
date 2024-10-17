document.addEventListener("DOMContentLoaded", function () {
    var options = {
        chart: {
            type: 'pie',
            height: '400px'
        },
        series: [44, 55, 13, 43, 22], // Tus datos aquí
        labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'], // Tus etiquetas aquí
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 300
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
    };

    var chart = new ApexCharts(document.querySelector("#pieChart"), options);
    chart.render();
});
