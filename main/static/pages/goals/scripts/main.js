function main (linked_options, goal_list) {

    linked_options =  JSON.parse(linked_options);
    goal_list = JSON.parse(goal_list);

    var notif = new Notifications();
    notif.check_notifications();

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
    title_panel.AddTitle('Daily Hourly Limit');

    // Check for notifications.


    /**
     *
     * SET UP PANELS FOR ALL PLATFORMS
     *
     * @type {Panel}
     */

    // Set up facebook panel
    const facebook_panel = new Panel('panel2', '25%', '50vh');
    facebook_panel.AddTitle('Facebook ');
    const fb_contents = new LinkedPlatform(facebook_panel, 'facebook', '/static/images/icons/facebook.png', '250px')
    fb_contents.add_button();

    // Insert youtube panel and icon
    const netflix_panel = new Panel('panel3', '25%', '50vh');
    netflix_panel.AddTitle('Netflix ');
    const netflix_contents = new LinkedPlatform(netflix_panel, 'netflix', '/static/images/icons/netflix.png', '250px')
    netflix_contents.add_button();

     // Insert youtube panel and icon
    const youtube_panel = new Panel('panel4', '25%', '50vh');
    youtube_panel.AddTitle('Youtube ');
    const yt_contents = new LinkedPlatform(youtube_panel, 'youtube', '/static/images/icons/youtube.png', '250px')
    yt_contents.add_button();

    // Insert Google panel and icon
    const google_panel = new Panel('panel5', '25%', '50vh');
    google_panel.AddTitle('Google ');
    const google_contents = new LinkedPlatform(google_panel, 'google', '/static/images/icons/google.png', '250px')
    google_contents.add_button();

    /**
     *
     * SET UP CONNECTION STATUS IN BUTTONS FOR ALL PLATFORMS
     *
     */

    span_arr = [0, 0, 0, 0];

    // Display facebook connection
    if (linked_options['facebook'] == 1) {
        fb_contents.add_form('', 0);
        fb_contents.display_disconnect('');
        fb_contents.disable_button()
    } else {
        var fb_goal = goal_list['facebook'];
        fb_contents.add_form('Update your daily time limit?', fb_goal);
        fb_contents.display_connect(fb_goal);
        span_arr[0] = 1;
    }

    // Display youtube connection
    if (linked_options['youtube'] == 1) {
        yt_contents.add_form('', 0);
        yt_contents.display_disconnect('');
        yt_contents.disable_button();
    } else {
        var yt_goal = goal_list['youtube'];
        yt_contents.add_form('Update your daily time limit?', yt_goal);
        yt_contents.display_connect(yt_goal);
        span_arr[1] = 1;
    }

    // Display netflix connection
    if (linked_options['netflix'] == 1) {
        netflix_contents.add_form('', 0);
        netflix_contents.display_disconnect('');
        netflix_contents.disable_button();
    } else {
        var netflix_goal = goal_list['netflix'];
        netflix_contents.add_form('Update your daily time limit?', netflix_goal);

        netflix_contents.display_connect(netflix_goal);
        span_arr[2] = 1;
    }

    // Display google connection
    if (linked_options['google'] == 1) {
        google_contents.add_form('', 0);
        google_contents.display_disconnect('');
        google_contents.disable_button();
    } else {
        var google_goal = goal_list['google'];
        google_contents.display_connect(google_goal);
        google_contents.add_form('Update your daily time limit?', google_goal);
        span_arr[3] = 1;
    }


    /**
     *
     * Set up all modals interaction for all platforms
     * @type {HTMLElement}
     */

    // Opening Facebook modal
    var modal1 = document.getElementById( 'facebook-modal');
    var btn1 = document.getElementById('facebook-button');
    btn1.onclick = function() { modal1.style.display = 'block'; };

    // Opening Netflix modal
    var modal2 = document.getElementById( 'netflix-modal');
    var btn2 = document.getElementById('netflix-button');
    btn2.onclick = function() {modal2.style.display = 'block';};

    // Opening Youtube modal
    var modal3 = document.getElementById( 'youtube-modal');
    var btn3 = document.getElementById('youtube-button');
    btn3.onclick = function() {modal3.style.display = 'block';};

    // Opening Google modal
    var modal4 = document.getElementById( 'google-modal');
    var btn4 = document.getElementById('google-button');
    btn4.onclick = function() {modal4.style.display = 'block';};

    // handle closing modals
    $('.close').click(function(event) {
        modal1.style.display = 'none';
        modal2.style.display = 'none';
        modal3.style.display = 'none';
        modal4.style.display = 'none';
    });

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



    /**
     *
     * If user confirms, update platform goal in database.
     * @type {Function}
     */

    document.getElementById('facebook-confirm').onclick = function () {

        fb_contents.update_button_text('Updating...');

        // Read in goal value
        var goal_val = fb_contents.get_goal();
        console.log("current goal is:" ,goal_val)

        // Update goal with ajax call
        update_goals(goal_val,'facebook', fb_contents, modal1);
    };

    document.getElementById('netflix-confirm').onclick = (function () {
        netflix_contents.update_button_text('Updating...');

        // Read in goal value
        var goal_val = netflix_contents.get_goal();
        console.log("current goal is:", goal_val);

        // Update goal with ajax call
        update_goals(goal_val,'netflix', netflix_contents, modal2);
    });

    document.getElementById('youtube-confirm').onclick = (function () {
        yt_contents.update_button_text('Updating...');

          // Read in goal value
        var goal_val = yt_contents.get_goal();
        console.log("current goal is:" ,goal_val);

        // Update goal with ajax call
        update_goals(goal_val,'youtube', yt_contents, modal3)
    });

    document.getElementById('google-confirm').onclick = (function () {
        google_contents.update_button_text('Updating...');

        // Read in goal value
        var goal_val = google_contents.get_goal();
        console.log("current goal is:", goal_val);

        // Update goal with ajax call
        update_goals(goal_val,'google', google_contents,modal4);
    });


    function update_goals(goal_val, platform, contents, modal) {
         $.ajax({
        url: '/ajax/update_goal',
        data: {
            'platform': platform,
            'goal':goal_val
        },
        dataType: 'json',
        success: function(data) {
            // Close the modal.
            if (data['result'] == 'success') {
                console.log('Successfully updated ' + platform + '\'s daily limit');
            } else {
                alert('Could not update ' + platform + '\'s daily limit. Please empty your caches and try again');
            }

            contents.update_button_text('Confirm');
            contents.display_connect(goal_val);
            modal.style.display = 'none';
        }
  });
    }
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
