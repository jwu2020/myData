function main (linked_options) {

    var notif = new Notifications();
    notif.check_notifications();

    linked_options = JSON.parse(linked_options)

    const topBar = new TitleBar('MY DATA', ['button'], 200, '/static/images/icon.png', '/static/images/icon_dark.png');

    const pages = {
        'Home': {
            'onclick' : function() {loadPage('main')},
            'image' : '/static/images/icons/home.png'
        },
        'Accounts': {
            'onclick' : function() {loadPage('accounts')},
            'image' : '/static/images/icons/account.png'
        },
        'Detailed': {
            'onclick' : function() {loadPage('detailed')},
            'image' : '/static/images/icons/search.png'
        },
        'Limits': {
            'onclick' : function() {loadPage('goals')},
            'image' : '/static/images/icons/clock.png'
        },
        'Logout': {
            'onclick' : function() {logout()},
            'image' : "/static/images/icons/logout.png"
        }
    };
    const sideBar = new HamburgerMenu('MY DATA', 'Main Page', pages);

    // Insert panel for title
    const title_panel = new Panel('panel1', '100%', '80px');
    title_panel.AddTitle('Link Accounts')

    // Create download button
    const download_button = document.createElement('button');
    download_button.id = "export";
    download_button.classList.add('export-button');
    download_button.onclick = function() {
        window.open(window.location.origin + '/download', '_blank');
    };

    const span = document.createElement('span');
    span.style['font-size'] = 'small';
    span.innerText = "Download All Data";
    download_button.appendChild(span);

    document.getElementById('panel1').firstChild.appendChild(download_button);




    /**
     *
     * SET UP PANELS FOR ALL PLATFORMS
     *
     * @type {Panel}
     */

    // Set up facebook panel
    const facebook_panel = new Panel('panel2', '25%', '50vh');
    facebook_panel.AddTitle('Facebook ');
    const fb_contents = new LinkedPlatform(facebook_panel, 'facebook', '/static/images/icons/facebook.png', '100%')
    fb_contents.add_button();



    // Insert yourtube panel and icon
    const netflix_panel = new Panel('panel3', '25%', '50vh');
    netflix_panel.AddTitle('Netflix ');
    const netflix_contents = new LinkedPlatform(netflix_panel, 'netflix', '/static/images/icons/netflix.png', '100%')
    netflix_contents.add_button();

     // Insert yourtube panel and icon
    const youtube_panel = new Panel('panel4', '25%', '50vh');
    youtube_panel.AddTitle('Youtube ');
    const yt_contents = new LinkedPlatform(youtube_panel, 'youtube', '/static/images/icons/youtube.png', '100%')
    yt_contents.add_button();

    // Insert Google panel and icon
    const google_panel = new Panel('panel5', '25%', '50vh');
    google_panel.AddTitle('Google! ');
    const google_contents = new LinkedPlatform(google_panel, 'google', '/static/images/icons/google.png', '100%')
    google_contents.add_button();

    /**
     *
     * SET UP CONNECTION STATUS IN BUTTONS FOR ALL PLATFORMS
     *
     */

    // Display facebook connection
    if (linked_options['facebook'] === 1) {
        fb_contents.add_modal("Would you like to connect? Insert your details below.");
        fb_contents.display_disconnect("Disconnected");

    } else {
        fb_contents.add_modal("Would you like to disconnect?");
        fb_contents.display_connect("Connected");
        fb_contents.hide_platform_details();
    }

    // Display youtube connection
    if (linked_options['youtube'] === 1) {
        yt_contents.add_modal("Would you like to connect? Insert your details below.");
        yt_contents.display_disconnect("Disconnected");

    } else {
        yt_contents.add_modal("Would you like to disconnect?");
        yt_contents.display_connect("Connected");
        yt_contents.hide_platform_details();
    }

    // Display netflix connection
    if (linked_options['netflix'] === 1) {
        netflix_contents.add_modal("Would you like to connect? Insert your details below.");
        netflix_contents.display_disconnect("Disconnected");

    } else {
        netflix_contents.add_modal("Would you like to disconnect?");
        netflix_contents.display_connect("Connected");
        netflix_contents.hide_platform_details();
    }

    // Display google connection
    if (linked_options['google'] == 1) {
        google_contents.add_modal("Would you like to connect? Insert your details below.");
        google_contents.display_disconnect("Disconnected");

    } else {
        google_contents.add_modal("Would you like to disconnect?");
        google_contents.display_connect("Connected");
        google_contents.hide_platform_details();
    }


    /**
     *
     * Set up all modals for all platforms
     * @type {HTMLElement}
     */
    // Facebook modal
    var modal1 = document.getElementById( 'facebook-modal');
    var btn1 = document.getElementById('facebook-button');
    btn1.onclick = function() {modal1.style.display = "block";};

    // Netflix
    var modal2 = document.getElementById( 'netflix-modal');
    var btn2 = document.getElementById('netflix-button');
    btn2.onclick = function() {modal2.style.display = "block";};

    // Youtube
    var modal3 = document.getElementById( 'youtube-modal');
    var btn3 = document.getElementById('youtube-button');
    btn3.onclick = function() {modal3.style.display = "block";};

    // Google
    var modal4 = document.getElementById( 'google-modal');
    var btn4 = document.getElementById('google-button');
    btn4.onclick = function() {modal4.style.display = "block";};

     // Handle closer buttons
     document.onclick = function(event) {
        if (event.target == modal1) {
            modal1.style.display = 'none';
        }
        else if (event.target == modal2) {
            modal2.style.display = 'none';
        }
        else if (event.target == modal3) {
            modal3.style.display = 'none';
        }
        else if (event.target == modal3) {
            modal3.style.display = 'none';
        }
        else if (event.target == modal4) {
            modal4.style.display = 'none';
        }
    };

     $('.close').click( function() {
        modal1.style.display = 'none';
        modal2.style.display = 'none';
        modal3.style.display = 'none';
        modal4.style.display = 'none';
    });


    /**
     *
     * If user confirms, connect or disconnect platform with database.
     * @type {Function}
     */

    document.getElementById("facebook-confirm").onclick = (function () {
        let status = fb_contents.check_status();
        document.getElementById("facebook-confirm").innerText = "Updating...";

        if (status === 0) {
            disconnect_platform('facebook', modal1, fb_contents);
        } else {
            // Update facebook login details
            const fb_username = fb_contents.get_platform_username();
            const fb_password = fb_contents.get_platform_password();
            connect_platform( 'facebook', fb_username, fb_password,  modal1, fb_contents);
        }
    });

    document.getElementById("netflix-confirm").onclick = (function () {
        let status = netflix_contents.check_status();
        document.getElementById("netflix-confirm").innerText = "Updating...";

        if (status === 0) {
            disconnect_platform('netflix', modal2, netflix_contents);
        } else {
            const netflix_username = netflix_contents.get_platform_username();
            const netflix_password = netflix_contents.get_platform_password();
            connect_platform( 'netflix', netflix_username, netflix_password, modal2, netflix_contents);
        }
    });


    document.getElementById("youtube-confirm").onclick = (function () {
        let status = yt_contents.check_status();
        document.getElementById("youtube-confirm").innerText = "Updating...";

        // If current state is connected, we want to disconnect.
        if (status === 0) {
            disconnect_platform('youtube', modal3, yt_contents)
            // If current state is disconnected, we know user will next link up account. Need to ensure that input form is ready.
            // Before we have connected, we need to hide form so when they next disconnect,they w0on't see the form.
        } else{
            const youtube_username = yt_contents.get_platform_username();
            const youtube_password = yt_contents.get_platform_password();
            connect_platform('youtube', youtube_username, youtube_password, modal3, yt_contents);
        }
    });

    document.getElementById("google-confirm").onclick = (function () {
        let status = google_contents.check_status();
        document.getElementById("google-confirm").innerText = "Updating...";

        if (status === 0) {
            disconnect_platform('google', modal4, google_contents);
        } else {
            const google_username = google_contents.get_platform_username();
            const google_password = google_contents.get_platform_password();
            connect_platform('google', google_username, google_password, modal4, google_contents);
        }
    });
}

// Function to disconnect platform
function disconnect_platform(platform, modal, contents) {
    contents.hide_platform_details();
    $.ajax({
        url: '/ajax/disconnect',
        data: {
            'platform': platform
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
            document.getElementById(platform + '-button').classList.remove('connected');
            document.getElementById(platform + '-button').classList.add('disconnected');
            document.getElementById(platform + '-button').innerText = "Disconnected";
            modal.style.display = "none";
            document.getElementById(platform + '-confirm').innerText = 'Confirm';
            document.getElementById(platform + '-prompt').innerText = 'Would you like to connect? Insert your details below.';

             contents.show_platform_details();
        }
  });
}

// Start polling data from specified platform by triggering python scripts
function trigger_polling(platform, platform_email, platform_password) {
    console.log("trigger polling: ", platform, platform_email, platform_password);
    // Update status of database
    $.ajax({
        url: '/poll',
        data: {
            'platform': platform,
            'platform_email': platform_email,
            'platform_password': platform_password,
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
        }
    });
}

// function to connect to platform
function connect_platform(platform, platform_email, platform_password, modal, contents)  {
    contents.show_platform_details();

    // Update status of database
    $.ajax({
        url: '/ajax/connect',
        data: {
            'platform': platform,
            'platform_email': platform_email,
            'platform_password': platform_password,
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
            document.getElementById(platform+'-button').classList.remove('disconnected');
            document.getElementById(platform+'-button').classList.add('connected');
            document.getElementById(platform+'-button').innerText = "Connected";
            modal.style.display = "none";
            document.getElementById(platform+"-confirm").innerText = "Confirm";
            document.getElementById(platform+'-prompt').innerText = "Would you like to disconnect?";
            contents.hide_platform_details();
            trigger_polling(platform, platform_email, platform_password)
        }
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