document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#datePicker", {
        dateFormat: "D d-M-Y",
        onChange: function(selectedDates, dateStr, instance) {
            console.log("Selected date is: ", dateStr);
        }
    });

    const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
    const monthlyChart = new Chart(monthlyCtx, {
        type: 'line',
        data: {
            labels: visualizationData.monthly.labels,

            datasets: [{
                label: 'Day expense',
                data: visualizationData.monthly.values,
                borderColor: 'rgba(58, 123, 213, 1)',
                backgroundColor: 'rgba(58, 123, 213, 0.2)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                filter: {
                    propagate: false
                },
                legend: {
                    position: 'top',
                    labels: {
                        color: 'rgba(44, 44, 84, 0.8)'
                    }
                },
                title: {
                    display: true,
                    text: "Monthly Expenditure Tracker",
                    color: 'rgba(21, 8, 95, 0.87)',
                    font: {
                        size: 25,
                        family: "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif"
                    }
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(3, 44, 103, 0.8)',
                    titleFont: {
                        size: 16,
                        family: "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif"
                    },
                    bodyFont: {
                        size: 14
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        color: 'rgba(44, 44, 84, 0.8)',
                        font: {
                            size: 16
                        }
                    },
                    ticks: {
                        minRotation: 30,
                        maxRotation: 30
                    },
                    grid: {
                        color: 'rgba(200, 200, 200, 0.3)'
                    },
                    beginAtZero: true
                },
                y: {
                    title: {
                        display: true,
                        text: 'Expense',
                        color: 'rgba(44, 44, 84, 0.8)',
                        font: {
                            size: 16
                        }
                    },
                    ticks: { color: 'rgb(13, 13, 58)' },
                    grid: {
                        color: 'rgba(200, 200, 200, 0.3)'
                    }
                }
            },
            elements: {
                point: {
                    radius: 5,
                    hoverRadius: 7,
                    hitRadius:10
                }
            }
        }
    });

    const weeklyCtx = document.getElementById('weeklyChart').getContext('2d');
    const weeklyChart = new Chart(weeklyCtx, {
        type: 'bar',
        data: {
            labels: visualizationData.weekly.labels,

            datasets: [{
                label: "Day's expense",
                data: visualizationData.weekly.values,
                borderColor: 'rgba(128, 0, 128, 1)',
                backgroundColor: [
                    'rgba(147, 112, 219, 0.8)',
                    'rgba(186, 85, 211, 0.8)',
                    'rgba(218, 112, 214, 0.8)',
                    'rgba(221, 160, 221, 0.8)',
                    'rgba(238, 130, 238, 0.8)',
                    'rgba(153, 50, 204, 0.8)',
                    'rgba(148, 0, 211, 0.8)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Weekly Expenditure Tracker',
                    color: '#4B0082',
                    font: {
                        size: 24,
                        family: "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif"
                    }
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(75, 0, 130, 0.8)',
                    titleFont: {
                        size: 16,
                        family: "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif"
                    },
                    bodyFont: {
                        size: 14
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        color: '#8A2BE2',
                        font: {
                            size: 16,
                            family: "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif"
                        }
                    },
                    grid: {
                        color: 'rgba(75, 0, 130, 0.2)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Expense',
                        color: '#8A2BE2',
                        font: {
                            size: 16,
                            family: "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif"
                        }
                    },
                    grid: {
                        color: 'rgba(75, 0, 130, 0.2)'
                    }
                }
            },
            elements: {
                bar: {
                    borderRadius: 5,
                    hoverBackgroundColor: 'rgba(128, 0, 128, 0.9)',
                    hoverBorderColor: 'rgba(75, 0, 130, 1)'
                }
            }
        }
    });

    const pieCtx = document.getElementById('pieChart').getContext('2d');
    const incomePieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: visualizationData.pie.labels,
            datasets: [{
                data: visualizationData.pie.values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(201, 203, 207, 0.6)'
                ],
                hoverBackgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(201, 203, 207, 0.8)'
                ],
                hoverOffset: 30
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 20,
                    bottom: 30
                }
            },
            plugins: {
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(139, 0, 0, 0.8)',
                    titleFont: {
                        size: 16,
                        family: "'Arial', Calibri, 'Trebuchet MS', sans-serif"
                    },
                    bodyFont: {
                        size: 14
                    }
                },
                legend: {
                    position: 'right',
                    labels: {
                        boxWidth: 12,
                        padding: 20
                    }
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const datePicker = document.getElementById('datePicker');
    datePicker.addEventListener('change', function() {

        const selectedDate = this.value;
        const formattedDate = new Date(selectedDate).toLocaleDateString('en-IN', {
            weekday: 'short', day: '2-digit', month: 'short', year: 'numeric'
        });
        const urlDate = formattedDate.replace(/, /g, '-').replace(/ /g, '-');

        window.location.href = `/dashboard?date=${urlDate}`;
    });

    $('#journalTable').DataTable({
        responsive: true,
        pageLength: 5,
        order: [[1, 'asc']],
        language: {
            search: 'Search:',
            paginate: {
                previous: '<i class = "fas fa-angle-left"></i>',
                next: '<i class = "fas fa-angle-right"></i>'
            }
        },
        columnDefs: [
            {
                targets: 4,
                className: 'entry-note'
            }
        ]
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const addTransactionButton = document.getElementById('add-transaction');
    const transactionModal = document.getElementById('transactionModal');

    addTransactionButton.addEventListener('click', function() {
        $(transactionModal).modal('show');
    });

    $('#transactionTime').clockTimePicker();

    $(transactionModal).on('show.bs.modal', function() {
        $('#transactionForm')[0].reset();
        $('#amountError, #typeError, #timeError').hide();

        const now = new Date();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
        $('#transactionTime').val(formattedTime);
    });

    function parseCustomDateFormat(dateStr) {
        const [dayName, day, monthName, year] = dateStr.split(/[\s-]+/);
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        const monthIndex = monthNames.indexOf(monthName);
        if(monthIndex == -1) { throw new Error('Invalid month name encountered while parsing.'); }

        return `${year}-${(monthIndex + 1).toString().padStart(2, '0')}-${day.padStart(2, '0')}`;
    }

    window.submitTransaction = function() {
        const amount = $('#transactionAmount').val();
        const type = $('#transactionType').val();
        const note = $('#transactionNote').val();
        const time = $('#transactionTime').val();

        let isValid = true;

        if(amount <= 0) {
            $('#amountError').show();
            isValid = false;
        } else {
            $('#amountError').hide();
        }
        if(!type) {
            $('#typeError').show();
            isValid = false;
        } else {
            $('#typeError').hide();
        }
        if(!time) {
            $('#timeError').show();
            isValid = false;
        } else {
            $('#timeError').hide();
        }

        if(isValid) {
            const date = parseCustomDateFormat($('#datePicker').val());
            const transactionDateTime = new Date(`${date}T${time}:00`);

            $.post('/add-transaction', {
                amount: amount,
                type: type,
                note: note,
                date: transactionDateTime.toISOString()
            }).done(function(response) {
                alert('Transaction added');
                $('#transactionModal').modal('hide');

            }).fail(function() {
                alert('ERROR: Failed to add transaction');
            });
        }
    }
});