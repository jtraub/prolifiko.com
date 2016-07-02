require('./index.scss');

var $ = require('jquery');

var LimitTextDone = false;
var MAX_WORDS = 100;

window.limitText = function limitText(textarea) {
    if (LimitTextDone) {
        return;
    }

    var submit = textarea.form.querySelector('input[type=submit]');

    var remaining = document.createElement('span');
    remaining.innerHTML = MAX_WORDS;

    var wrapper = document.createElement('div');
    wrapper.appendChild(remaining);
    wrapper.appendChild(document.createTextNode(' words remaining'));

    textarea.parentNode.appendChild(wrapper);

    textarea.addEventListener('input', function () {
        var words = this.value.split(' ').filter(function (word) {
            return word.length > 0;
        });
        var wordsLeft = MAX_WORDS - words.length;

        submit.disabled = words.length === 0;

        remaining.innerHTML = wordsLeft;
        remaining.style.color = wordsLeft >= 0 ? 'black' : 'red';
    });

    textarea.form.addEventListener('submit', function(event) {

        if (textarea.value.split(' ').length > MAX_WORDS) {
            alert('Too many words!');
            event.preventDefault();
            return false;
        }

        return true;
    });

    LimitTextDone = true;
};

var passwordInputs = document.querySelectorAll('input[type=password]');

passwordInputs.forEach(function (password) {
    var passwordShown = false;

    var toggle = document.createElement('button');
    toggle.innerHTML = 'Show password';

    toggle.addEventListener('click', function (event) {
        event.preventDefault();
        return false;
    });

    toggle.addEventListener('click', function () {
        passwordShown = !passwordShown;
        toggle.innerHTML = (passwordShown ? 'Hide' : 'Show') + ' password';
        password.type = passwordShown ? 'text' : 'password';
    });

    password.parentNode.insertBefore(toggle, password.nextSibling);
});