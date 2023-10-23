function showError(){
    let errorDiv = document.querySelector('.invalid-feedback');
    errorDiv.classList.add('show');
}

function removeErrorError(){
    let errorDiv = document.querySelector('.invalid-feedback');
    errorDiv.classList.remove('show');
}

(function () {
    'use strict'

    var form = document.querySelector('.needs-validation')
  
    form.addEventListener('submit', function (event) {
        let username = document.getElementById('playerUsername').value;
        if (username.length < 5 || username.length > 20) {
            showError();
            event.preventDefault();
            event.stopPropagation();
        }
        removeError();
        }, 
        false
    )
  })()