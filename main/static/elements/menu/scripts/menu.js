class HamburgerMenu {

    constructor(title, pageName, pages) {

        this.title = title;
        this.pageName = pageName
        this.pages = pages;

        let sideBar = document.createElement('div');
        sideBar.id = 'sideBar';
        sideBar.classList.add('menu-bar');

        let heading = document.createElement('h1');
        heading.classList.add('title-bar-heading');
        heading.classList.add('behind');
        heading.innerText = this.title;
        sideBar.appendChild(heading);

        let page = document.createElement('h1');
        page.classList.add('menu-bar-heading');
        page.classList.add('menu-hea');
        page.innerText = this.pageName;
        sideBar.appendChild(page);

        let menuToggle = document.createElement('div');
        menuToggle.id = 'menuToggle';
        let checkbox = document.createElement('input');
        checkbox.id = 'menuToggleCheckbox'
        checkbox.type = 'checkbox';
        checkbox.onclick = function() {
            if (sideBar.classList.contains('in')) {
                sideBar.classList.remove('in');
                document.removeEventListener("mousedown", closeMenu);
            } else {
                sideBar.classList.add('in');
                document.addEventListener("mousedown", closeMenu);
            }
        }

        menuToggle.appendChild(checkbox);
        menuToggle.appendChild(document.createElement('span'));
        menuToggle.appendChild(document.createElement('span'));
        menuToggle.appendChild(document.createElement('span'));
        menuToggle.appendChild(document.createElement('div'));
        page.appendChild(menuToggle);


        for(let page in pages) {

            let option = document.createElement('h1');
            option.classList.add('menu-option');
            option.classList.add('sub-menu-option');
            option.innerText = page;

            let link = document.createElement('a');
            if (page === 'Detailed') {
                option.id = 'Detailed';
                link.onclick = ()=>{
                    console.log(document.getElementById('subOptions').style.maxHeight);
                    if (document.getElementById('subOptions').style.maxHeight === '144px') {
                        document.getElementById('subOptions').style.maxHeight = '0px';
                    } else {
                        document.getElementById('subOptions').style.maxHeight = '144px';
                    }
                };
            } else {
                link.onclick = pages[page]['onclick'];
            }

            let icon = document.createElement('img');
            icon.src = pages[page].image;
            icon.classList.add('sub-menu-icon');
            option.appendChild(icon);
            link.appendChild(option);
            sideBar.appendChild(link);

            if (page === 'Detailed') {
                let subOptions = document.createElement('div');
                subOptions.id = 'subOptions';
                let subPages = {
                    Facebook: {
                        'onclick': function() {loadPage('detailed_fb');},
                        image: '/static/images/icons/facebook_line.png',
                    },
                    Netflix: {
                        'onclick': function() {loadPage('detailed_netflix');},
                        image: '/static/images/icons/netflix_line.png',
                    },
                    YouTube: {
                        'onclick': function() {loadPage('detailed_yt');},
                        image: '/static/images/icons/youtube_line.png',
                    },
                    Google: {
                        'onclick': function() {loadPage('detailed_google');},
                        image: '/static/images/icons/google_line.png',
                    }
                };
                for (let subPage in subPages) {
                    let subLink = document.createElement('a');
                    subLink.id = 'first';
                    subLink.onclick = subPages[subPage]['onclick'];
                    console.log(subLink.onclick);
                    let subOption = document.createElement('h1');
                    subOption.classList.add('menu-option');
                    subOption.classList.add('sub-menu-option');
                    subOption.classList.add('sub-sub-menu-option');
                    subOption.innerText = subPage;


                    let subIcon = document.createElement('img');
                    subIcon.src = subPages[subPage].image;
                    subIcon.classList.add('sub-menu-icon');
                    subIcon.classList.add('sub-sub-menu-icon');
                    subOption.appendChild(subIcon);

                    subLink.append(subOption);
                    subOptions.appendChild(subLink);
                }
                sideBar.appendChild(subOptions);
            }
        }

        document.body.prepend(sideBar);

        let blocker = document.createElement('div');
        blocker.id = 'blocker';
        document.body.prepend(blocker);
    }
}


function closeMenu(event) {
    if (event.target.id === 'menuToggleCheckbox' || event.target.id === 'Detailed' ) return;
    if (event.button !== 0) return;
    document.getElementById('menuToggleCheckbox').click();
    document.removeEventListener('mousedown', closeMenu);
}


function loadPage(page) {
    console.log(page);
    // let preload = document.createElement('link');
    // preload.rel = 'preload';
    // preload.href = '/' + page;
    // document.head.appendChild(preload);
    setTimeout( function(){
        window.location = page
    },350)
}