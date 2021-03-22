
let onLogin = true;
function main() {
    console.log('Login Page');

    const topBar = new TitleBar('MY DATA', ['button'], 200, "/static/images/icon.png", "/static/images/icon_dark.png");

    let radios = document.loginFrom.logOrSign;
    for (let i = 0; i < radios.length; i++) {
        radios[i].addEventListener('change', function() {
            onLogin = !onLogin;
            let signin_elements = document.getElementsByClassName('sign-in-element');
            if (onLogin) {
                for (let i = 0; i < signin_elements.length; i++) {
                    signin_elements[i].style.maxHeight = '0px';
                    setTimeout(function() {signin_elements[i].style.display = 'none'}, 500);
                }
                document.getElementById('login-button').value = 'Login';
                document.getElementById('login-bar').style.transform = 'translateX(0%)';
                document.getElementById('loginForm').style.minHeight = '350px';
            } else {
                for (let i = 0; i < signin_elements.length; i++) {
                    signin_elements[i].style.display = 'block';
                    signin_elements[i].style.maxHeight = String(document.getElementById('password').clientHeight + signin_elements.length) + 'px';
                }

                document.getElementById('login-button').value = 'Sign Up';
                document.getElementById('login-bar').style.transform = 'translateX(100%)';
                document.getElementById('loginForm').style.minHeight = String(document.getElementById('loginForm').clientHeight + signin_elements.length*document.getElementById('password').clientHeight + signin_elements.length)  + 'px';
            }
        });
    }
}

function submitForm(form) {
    try {
        let result = {};
        result.type = onLogin ? 'login' : 'sign-up';
        let failed = false;
        let form_elements = document.forms["loginFrom"].getElementsByClassName(result.type);

        for (let i = 0; i < form_elements.length; i++) {
            if (form_elements[i].value === '') {
                form_elements[i].style.animationName = 'shake';
                setTimeout(function() {form_elements[i].style.animationName = ''}, 500);
                failed = true;
            }
            result[form_elements[i].name] = form_elements[i].value;
        }
        if (failed) return;

        if (!onLogin) {
            if (!(form_elements.password.value === form_elements.password2.value)) {
                form_elements.password.style.animationName = 'shake';
                form_elements.password2.style.animationName = 'shake';
                form_elements.password2.select();
                setTimeout(function () {
                    form_elements.password.style.animationName = '';
                    form_elements.password2.style.animationName = '';
                }, 500);
                return;
            }
        }

        let xhr = new XMLHttpRequest();
        xhr.open("POST", '/login', true);
        xhr.setRequestHeader("X-CSRFToken", document.cookie.match(/csrftoken=([a-z,A-Z,0-9]+)/)[1]);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({value: result}));

        xhr.onload = function () {
            console.log('Response: ', JSON.parse(this.responseText));
            let response = JSON.parse(this.responseText);
            if (response.login === 'true') {
                document.location = '/';
            } else if(response.login === 'false') {
                document.getElementById('password').style.animationName = 'shake';
                setTimeout(function() {document.getElementById('password').style.animationName = ''}, 500);
                document.getElementById('password').select();
            } else if (response['sign-in'] === 'existing user') {
                document.getElementById('username').style.animationName = 'shake';
                setTimeout(function() {document.getElementById('username').style.animationName = ''}, 500);
                document.getElementById('username').select();
            } else if (response['sign-in'] === 'true') {
                document.location = '/accounts';
            }
        };

    } catch (error) {
        console.warn(error);
        return false;
    }
}