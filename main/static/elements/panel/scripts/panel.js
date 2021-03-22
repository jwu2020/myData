class Panel {
    constructor(id, width, height) {
        this.panel = document.createElement('div');
        this.panel.id = id;
        this.panel.classList.add('panel');

        this.outer_panel = document.createElement('div');
        this.outer_panel.style.width = width;
        this.outer_panel.style.minHeight = height || '100%';
        this.outer_panel.classList.add('outer-panel');
        this.outer_panel.appendChild(this.panel);

        document.getElementById('inBody').appendChild(this.outer_panel);
        console.log(this.panel.clientWidth);
    }

    AddTitle(title_text) {
        this.title = document.createElement('h2');
        this.title.classList.add('title_content');
        this.title.innerText = title_text;
        this.panel.appendChild(this.title);
    }
}