function qtd_count_operations() {
    var labels = []
    var quantidade = []
    $.ajax({
    url: '/chart_operations/',
    dataType: 'json',
  }).done(function (e) {
    labels = []
    quantidade = []
    e.count_operations_chart.forEach(function (value) {
      labels.push(value.operation_type)
      quantidade.push(value.my_count)
    });
    //console.log(labels, quantidade)


    new Chart(document.getElementById("chart-sdgw-01"), {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3c8dbc","#EE7402", "#773DBD"],
        data: quantidade
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
      }

    }

});

})

}
qtd_count_operations()

//   Funcção que retorna os valores do PROXIES 3 --------------


function qtd_count_operations2() {
    var labels2 = []
    var quantidade2 = []
    $.ajax({
    url: '/chart_operations/',
    dataType: 'json',
  }).done(function (e) {
    labels2 = []
    quantidade2 = []
    e.count_operations_chart2.forEach(function (value) {
      labels2.push(value.operation_type)
      quantidade2.push(value.my_count)
    });
    //console.log(labels, quantidade)


    new Chart(document.getElementById("chart-sdgw-02"), {
    type: 'pie',
    data: {
      labels: labels2,
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3c8dbc","#EE7402", "#773DBD"],
        data: quantidade2
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
      }

    }

});

})

}
qtd_count_operations2()


//   Funcção que retorna os valores do PROXIES 3 --------------
function qtd_count_operations3() {
    var labels3 = []
    var quantidade3 = []
    $.ajax({
    url: '/chart_operations/',
    dataType: 'json',
  }).done(function (e) {
    labels3 = []
    quantidade3 = []
    e.count_operations_chart3.forEach(function (value) {
      labels3.push(value.operation_type)
      quantidade3.push(value.my_count)
    });
    //console.log(labels, quantidade)


    new Chart(document.getElementById("chart-sdgw-03"), {
    type: 'pie',
    data: {
      labels: labels3,
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3c8dbc","#EE7402", "#773DBD"],
        data: quantidade3
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
      }

    }

});

})

}
qtd_count_operations3()



//   Funcção que retorna os valores do PROXIES 4 --------------
function qtd_count_operations4() {
    var labels4 = []
    var quantidade4 = []
    $.ajax({
    url: '/chart_operations/',
    dataType: 'json',
  }).done(function (e) {
    labels4 = []
    quantidade4 = []
    e.count_operations_chart4.forEach(function (value) {
      labels4.push(value.operation_type)
      quantidade4.push(value.my_count)
    });
    //console.log(labels, quantidade)


    new Chart(document.getElementById("chart-sdgw-04"), {
    type: 'pie',
    data: {
      labels: labels4,
      datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3c8dbc","#EE7402", "#773DBD"],
        data: quantidade4
      }]
    },
    options: {
      responsive: true,
      title: {
        display: true,
      }

    }

});

})

}
qtd_count_operations4()