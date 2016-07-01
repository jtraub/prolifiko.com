var LimitTextDone = false;
var MAX_WORDS = 100;

function limitText(textarea) {
    if (LimitTextDone) {
        return;
    }

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
}