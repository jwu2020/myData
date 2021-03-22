

function main (platform) {

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
        'Goals': {
            'onclick' : function() {loadPage('goals')},
            'image' : "/static/images/icons/target.png"
        },
        'Logout': {
            'onclick' : function() {setTimeout( function(){alert('Logged Out')},300)},
            'image' : "/static/images/icons/logout.png"
        }
    };
    const sideBar = new HamburgerMenu('MY DATA', 'Main Page', pages);

    document.getElementById('inBody').style.height= '950px';

    // Add panel with simple message alerting user to connect their platform.
    const panel1 = new Panel('panel1', '100%', '100%');
    panel1.panel.style['box-shadow']= 'none';
    const message_container = document.createElement('div');
    message_container.style.height = 'inherit';
    const message = document.createElement('p');
    message.classList.add('empty-message');
    message.innerText = platform + ' is disconnected. Please link it back in Accounts to view this page.';
    message_container.appendChild(message);
    panel1.panel.appendChild(message_container);


}
