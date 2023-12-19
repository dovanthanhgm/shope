var languageSelection = document.getElementById('language_selection');
var submitBtn = document.getElementById('submit_btn');

languageSelection.addEventListener('change', function () {
    submitBtn.click();
});