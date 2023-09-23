document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.getElementById('darkModeToggle');
    var darkModeStylesheet = document.getElementById('darkModeStylesheet');
    var bodyElement = document.body;

    var darkMode = localStorage.getItem('darkMode') === 'enabled';

    if (darkMode) {
        darkModeStylesheet.removeAttribute('disabled');
        bodyElement.classList.add('dark-mode');
        toggle.checked = true;
    } else {
        darkModeStylesheet.setAttribute('disabled', 'true');
        bodyElement.classList.remove('dark-mode');
        toggle.checked = false;
    }

    toggle.addEventListener('change', function() {
        if (this.checked) {
            darkModeStylesheet.removeAttribute('disabled');
            bodyElement.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        } else {
            darkModeStylesheet.setAttribute('disabled', 'true');
            bodyElement.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
        }
    });
});
