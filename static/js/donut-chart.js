document.addEventListener('DOMContentLoaded', function () {
  const purchaseData = JSON.parse(localStorage.getItem('purchaseData')) || [];

  if (purchaseData.length > 0) {
      // Mostrar gráfico y botones si hay datos
      document.getElementById('donutChartContainer').style.display = 'block';
      document.getElementById('noDataMessage').style.display = 'none';
      document.getElementById('buttonsContainer').style.display = 'block';

      // Extraer descripciones y datos
      const labels = purchaseData.map(item => item.description);
      const data = purchaseData.map(item => parseFloat(item.price.replace(/[^0-9.-]+/g, "")) * item.quantity);

      var optionsDonut = {
          series: data,
          chart: {
              type: 'donut',
              height: 500,
              toolbar: {
                  show: true,  // Mostrar la barra de herramientas
                  tools: {
                      download: true  // Habilitar la opción de descarga
                  }
              }
          },
          labels: labels,
          legend: {
              position: 'bottom',
              labels: {
                  colors: '#1E3A8A'
              }
          },
          plotOptions: {
              pie: {
                  donut: {
                      size: '75%'
                  }
              }
          },
          colors: ['#1E3A8A', '#4F46E5', '#6D28D9', '#9333EA', '#A855F7'],
          dataLabels: {
              enabled: true,
              style: {
                  colors: ['#fff']
              }
          },
          grid: {
              padding: {
                  top: 0,
                  bottom: 0
              }
          }
      };

      var donutChart = new ApexCharts(document.querySelector("#donutChart"), optionsDonut);
      donutChart.render();

      // Función para limpiar los datos del gráfico y eliminar de localStorage
      document.getElementById('clearChartButton').addEventListener('click', function () {
          // Limpiar datos del gráfico
          donutChart.updateSeries([[]]);

          // Eliminar datos de localStorage
          localStorage.removeItem('purchaseData');

          // Mostrar mensaje de no hay datos
          document.getElementById('donutChartContainer').style.display = 'none';
          document.getElementById('noDataMessage').style.display = 'block';
          document.getElementById('buttonsContainer').style.display = 'none';
      });

      // Función para descargar el gráfico como imagen
      document.getElementById('downloadChartButton').addEventListener('click', function () {
          donutChart.dataURI().then(function (uri) {
              var link = document.createElement('a');
              link.href = uri.imgURI;
              link.download = 'donut-chart.png';
              link.click();
          });
      });

  } else {
      // Ocultar gráfico y botones, mostrar mensaje de no hay datos
      document.getElementById('donutChartContainer').style.display = 'none';
      document.getElementById('noDataMessage').style.display = 'block';
      document.getElementById('buttonsContainer').style.display = 'none';
  }
});
