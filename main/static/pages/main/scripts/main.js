

// function main (username, pie_data, bar_data, bar_categories, db_status) {
function main (pie_data, bar_data, db_status, bar_categories) {
    if (db_status === 1) {
        console.warn("Cannot connect to database");
    }

    console.log(bar_categories);
    console.log(JSON.parse(bar_categories));

    var notif = new Notifications();
    notif.check_notifications();

    const topBar = new TitleBar('MY DATA', ['button'], 200, "/static/images/icon.png", "/static/images/icon_dark.png");

    const pages = {
        'Home': {
            'onclick' : function() {loadPage('main')},
            'image' : "/static/images/icons/home.png"
        },
        'Accounts': {
            'onclick' : function() {loadPage('accounts')},
            'image' : "/static/images/icons/account.png"
        },
        'Detailed': {
            'onclick' : function() {loadPage('detailed')},
            'image' : "/static/images/icons/search.png"
        },
        'Limits': {
            'onclick' : function() {loadPage('goals')},
            'image' : "/static/images/icons/clock.png"
        },
        'Logout': {
            'onclick' : function() {logout()},
            'image' : "/static/images/icons/logout.png"
        }
    };

    const sideBar = new HamburgerMenu('MY DATA', 'Main Page', pages);

    const panel1 = new Panel('panel1', '30%');

    console.log((pie_data));

    let pie = Highcharts.chart(panel1.panel.id, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie',
            events: {
                load: function () {
                    console.log(this.reflow());
                    this.reflow();
                    // pie.reflow();
                }
            },
        },
        colors: ['#5a84c2', '#b84c4b', '#73bf4d', '#68bffd', '#de8201', '#f7da87'],
        credits: {
            enabled: false
        },
        title: {
            text: 'Hours Spent Today'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Portion',
            colorByPoint: true,
            data: JSON.parse(pie_data),
        }]
    });

    const panel2 = new Panel('panel2', '70%');

    const bars = Highcharts.chart(panel2.panel.id, {
        chart: {
            type: 'column'
        },
        colors: ['#5a84c2', '#b84c4b', '#73bf4d', '#68bffd', '#de8201', '#f7da87'],
        credits: {
            enabled: false
        },
        title: {
            text: 'Weekly Data Usage Overview'
        },
        xAxis: {
            categories: JSON.parse(bar_categories)
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Hours'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: ( // theme
                        Highcharts.defaultOptions.title.style &&
                        Highcharts.defaultOptions.title.style.color
                    ) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -30,
            verticalAlign: 'top',
            y: 25,
            floating: true,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: JSON.parse(bar_data),
    });


     // outer_panel = document.createElement('div');
     // outer_panel.style.width = '30%';
     // outer_panel.style.minHeight = '100%';
     // outer_panel.classList.add('outer-panel');

     // document.getElementById('inBody').appendChild(this.outer_panel);

    // // Create download button
    // const download_button = document.createElement('button');
    // download_button.id = "export";
    // download_button.classList.add('export-button');
    // download_button.style.verticalAlign = "middle";
    // download_button.style.width = "98%";
    // const span = document.createElement('span');
    // span.style['font-size'] = 'small';
    // span.innerText = "Export your data";
    // download_button.appendChild(span);
    //
    // outer_panel.appendChild(download_button);
    //
    // download_button.onclick = function() {
    //     console.log("clicked");
    //     console.log('username:', userName);
    //     window.open(window.location.href + 'download?username=' + userName, '_blank');
    // }


    //  const outer_panel = document.createElement('div');
    //  outer_panel.style.width = '30%';
    //  outer_panel.style.minHeight = '100%';
    //  outer_panel.classList.add('outer-panel');
    //
    //  document.getElementById('inBody').appendChild(outer_panel);
    //
    // // Create download button
    // const download_button = document.createElement('button');
    // download_button.id = "export";
    // download_button.classList.add('export-button');
    // download_button.style.verticalAlign = "middle";
    // download_button.style.width = "98%";
    // const span = document.createElement('span');
    // span.style['font-size'] = 'small';
    // span.innerText = "Export your data";
    // download_button.appendChild(span);
    //
    // outer_panel.appendChild(download_button);
    //
    // download_button.onclick = function() {
    //     window.open(window.location.href + 'download', '_blank');
    // }
}
//
// function check_notifications() {
//     $.ajax({
//         url: '/ajax/check_notifications',
//         data: {
//         },
//         dataType: 'json',
//
//         success: function(data) {
//             const arr = data['platform'];
//             const platforms = ''.concat(arr);
//             message = 'Daily limit reached: ' + platforms;
//             Notify(message, function() {})
//         }
//     });
// }
//
// function Notify(message, onclick) {
//     if (Notification.permission !== 'granted') {
//         Notification.requestPermission().then((result) => {
//             if (result === 'denied')
//                 console.log('Notification Permission Denied');
//             if (result === 'default')
//                 console.log('Notification Permission Dismissed.');
//         });
//     } else {
//         let notification = new Notification('MYDATA', {
//             icon: '/static/images/icon.png',
//             body: message,
//         });
//         notification.onclick = function() {onclick()}
//     }
// }

function logout() {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", '/logout', true);
    xhr.setRequestHeader("X-CSRFToken", document.cookie.match(/csrftoken=([a-z,A-Z,0-9]+)/)[1]);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({value: {'type': 'logout'}}));
    document.location = '/login';
    xhr.onload = function () {
        console.log('Response: ', this.responseText);
    };
}