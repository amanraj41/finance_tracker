document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#datePicker", {
        defaultDate: "today",
        dateFormat: "D d-M-Y",
        onChange: function(selectedDates, dateStr, instance) {
            console.log("Selected date is: ", dateStr);
        }
    });

    const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
    const monthlyChart = new Chart(monthlyCtx, {
        type: 'line',
        data: {
            labels: [],

            datasets: [{
                label: 'Monthly Expenditure Tracker',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });

    const weeklyCtx = document.getElementById('weeklyChart').getContext('2d');
    const weeklyChart = new Chart(weeklyCtx, {
        type: 'bar',
        data: {
            labels: [],

            datasets: [{
                label: 'Weekly Expenditure Tracker',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });

    const pieCtx = document.getElementById('incomePieChart').getContext('2d');
    const incomePieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Income', 'Spent', 'Remaining'],
            datasets: [{
                data: [],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(255, 206, 86, 0.6)'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });
});