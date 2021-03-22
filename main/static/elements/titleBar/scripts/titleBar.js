


class TitleBar {

    constructor(title, elements, hideHeight, image,  hiddenImage) {
        this.title = title;
        this.elements = elements;

        let titleBar = document.createElement('div');
        titleBar.classList.add('title-bar');

        let imgLink = document.createElement('a');
        imgLink.href = '';

        let icon = document.createElement('img');
        icon.src = image;
        icon.classList.add('title-icon')
        titleBar.appendChild(icon);

        let hiddenIcon = document.createElement('img');
        hiddenIcon.src =  hiddenImage;
        hiddenIcon.classList.add('title-icon')
        hiddenIcon.classList.add('behind')
        document.body.prepend(hiddenIcon);

        let heading = document.createElement('h1');
        heading.classList.add('title-bar-heading');
        heading.innerText = this.title;
        titleBar.appendChild(heading);
        document.body.prepend(titleBar);

        window.onscroll = function() {


            if (document.documentElement.scrollTop > hideHeight) {
                if (!titleBar.classList.contains('unstuck')) {
                    titleBar.classList.add('unstuck');
                    titleBar.style.top = document.documentElement.scrollTop + 'px';
                }

                if (parseInt(titleBar.style.top,10) < document.documentElement.scrollTop - titleBar.clientHeight) {
                    console.log('hi');

                    titleBar.style.top = (document.documentElement.scrollTop - titleBar.clientHeight) + 'px';
                }

            }

            if (titleBar.classList.contains('unstuck') && parseInt(titleBar.style.top,10) > document.documentElement.scrollTop) {
                titleBar.classList.remove('unstuck');
                titleBar.style.top = '0px';
            }
        }
    }
}




