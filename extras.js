function renderChart(canvasId, prediction) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Local', 'Empate', 'Visitante'],
      datasets: [{
        label: 'Probabilidades',
        data: [prediction.prob_home, prediction.prob_draw, prediction.prob_away],
        backgroundColor: ['#28a745', '#ffc107', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Distribución de Probabilidades' }
      },
      scales: {
        y: { beginAtZero: true, max: 1 }
      }
    }
  });
}
