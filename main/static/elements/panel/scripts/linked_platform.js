class LinkedPlatform {
    constructor(platform_panel, platform, image, width) {
        // Get image of icon
        this.platform_name = platform;
        this.platform_panel = platform_panel;
        this.platform_icon = document.createElement('img');
        this.platform_icon.src = image;
        this.platform_icon.classList.add('platform-icon');
        this.platform_icon.id = platform + '-icon';
        this.platform_icon.style.width = width || '250px';

        // Insert image into container, and add to panel
        this.platform_container =  document.createElement('div');
        this.platform_container.classList.add('platform-container');
        platform_panel.panel.appendChild(this.platform_container);
        this.platform_container.appendChild(this.platform_icon);
    }

    // Add confirmation button to connect or disconnect.
    add_button() {
        this.button = document.createElement('button');
        this.button.type = 'button';
        this.button.classList.add('block');
        this.button.classList.add('body');
        this.button.id = this.platform_name  + '-button';
        this.platform_panel.panel.appendChild(this.button);

    }

    // Set up pop up confirmation message.

    add_form(text, old_goal) {
        // Create modal container
        this.modal = document.createElement('div');
        this.modal.id = this.platform_name + "-modal";
        this.modal.classList.add("modal");

        // Create modal content
        this.modal_content = document.createElement('div');
        this.modal_content.classList.add('modal-content');
        this.close = document.createElement('span');
        this.close.classList.add('close');

        // Create text
        this.close.innerText = "x";
        this.close.classList.add('close');
        this.modal_text = document.createElement('p');
        this.modal_text.id = this.platform_name + "-prompt";
        this.modal_text.innerText = text;

        // Create form
        this.form = document.createElement('input');
        this.form.type = 'number';
        this.form.placeholder = old_goal;
        this.form.value = old_goal;
        this.form.classList.add('goal-text');
        this.form_container = document.createElement('div');

        // Create confirmation button
        this.confirm_button = document.createElement('button');
        this.confirm_button.id = this.platform_name + "-confirm";
        this.confirm_button.classList.add('confirm');
        this.confirm_button.innerText = "Confirm";

        // Link up content, modal and the page.
        this.modal_content.appendChild(this.close);
        this.modal_content.appendChild(this.modal_text);
        this.modal_content.appendChild(this.form_container);
        this.form_container.appendChild(this.form);
        this.form_container.appendChild(this.confirm_button);

        // this.modal_content.appendChild(this.confirm_button);
        this.modal.appendChild(this.modal_content);
        document.getElementById('modal-container').appendChild(this.modal);

    }


    add_modal(text) {
        // Create modal container
        this.modal = document.createElement('div');
        this.modal.id = this.platform_name + "-modal";
        this.modal.classList.add("modal");

        // Create modal content
        this.modal_content = document.createElement('div');
        this.modal_content.classList.add('modal-content');
        this.close = document.createElement('span');
        this.close.classList.add('close');

        // Create text
        this.close.innerText = "x";
        this.close.classList.add('close');
        this.modal_text = document.createElement('p');
        this.modal_text.id = this.platform_name + "-prompt";
        this.modal_text.innerText = text;

        // Create platform login inputs this.button.classList.add('disconnected');
        // if (this.button.classList[2] == 'disconnected') {
        console.log("Create form inputs");
        this.platform_details_container = document.createElement('div');
        this.platform_details_container.id = this.platform_name + '-login-input';

        this.platform_username = document.createElement('input');
        this.platform_username.type = 'text';
        this.platform_username.placeholder = 'username';
        this.platform_username.classList.add('platform-input');

        this.platform_password = document.createElement('input');
        this.platform_password.type = 'password';
        this.platform_password.placeholder = 'password';
        this.platform_password.classList.add('platform-input')
        this.platform_details_container.appendChild(this.platform_username);
        this.platform_details_container.appendChild(this.platform_password);


        // Create confirmation button
        this.confirm_button = document.createElement('button');
        this.confirm_button.id = this.platform_name + "-confirm";
        this.confirm_button.classList.add('confirm');
        this.confirm_button.innerText = "Confirm";

        // Link up content, modal and the page.
        this.modal_content.appendChild(this.close);
        this.modal_content.appendChild(this.modal_text);
        // if (this.button.classList[2] == 'disconnected') {

        console.log("linking form inputs");
        this.modal_content.appendChild(this.platform_details_container);

        this.modal_content.appendChild(this.confirm_button);
        this.modal.appendChild(this.modal_content);
        document.getElementById('modal-container').appendChild(this.modal);

    }

    // If platform is disconnected, display disconnect attributes.
    display_disconnect(text) {
        this.button.classList.add('disconnected');
        this.button.innerText = text;
        // this.platform_username.style.display = 'block';
        // this.platform_password.style.display = 'block';

    }


    // If platform is connected, display connected attributes.
    display_connect(text) {
        this.button.classList.add('connected');
        this.button.innerText = text;
        // this.platform_username.style.display = 'none';
        // this.platform_password.style.display = 'none';
    }

    // Check whether the platform is linked or not.
    check_status() {
        if (this.button.innerText === "Disconnected") {
            return 1;
        } else {
            return 0;
        }
    }

    disable_button() {
        this.button.style.pointerEvents = 'none';
    }

    update_button_text(text) {
        this.confirm_button.innerText = text;
    }

    get_goal() {
        console.log("getting goal:", this.form.value);
        return this.form.value ;
    }

    get_platform_username() {
        console.log(this.platform_username.value);
        return this.platform_username.value;
    }

    get_platform_password() {
        return this.platform_password.value;
    }

    hide_platform_details() {
        this.platform_username.style.display = 'none';
        this.platform_password.style.display = 'none';
    }

    show_platform_details() {
        this.platform_username.style.display = 'block';
        this.platform_password.style.display = 'block';
    }


}