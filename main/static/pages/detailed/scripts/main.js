

function main (line_data, x_labels, title, db_status) {


     if (db_status == 1) {
        console.warn("Cannot connect to database");
    } else {
         var notif = new Notifications();
         notif.check_notifications();

     }


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

    const panel1 = new Panel('panel1', '100%', '100%');

    let line  = Highcharts.chart(panel1.panel.id, {
        chart: {
            type: 'line',
            events: {
                load: function () {
                    console.log(this.reflow());
                    this.reflow();
                }
            },
        },
        credits: {
            enabled: false
        },
        title: {
            text: title
        },
        subtitle: {
            text: 'See how you are spending your time on ' + title
        },
        xAxis: {
            categories: JSON.parse(x_labels)
        },
        yAxis: {
            title: {
                text: 'Hours'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        },
        series: JSON.parse(line_data)
    });

}



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