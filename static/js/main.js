function showError(){
    let errorDiv = document.querySelector('.invalid-feedback');
    errorDiv.classList.add('show');
}

function removeErrorError(){
    let errorDiv = document.querySelector('.invalid-feedback');
    errorDiv.classList.remove('show');
}

function validateUsername(username){
    validator = /^[a-z0-9]{5,20}$/;
    return validator.test(username);
}

(function () {
    'use strict'

    var form = document.querySelector('.needs-validation')
  
    form.addEventListener('submit', function (event) {
        let username = document.getElementById('playerUsername').value;
        if (!validateUsername(username)) {
            showError();
            event.preventDefault();
            event.stopPropagation();
        }
        removeError();
        }, 
        false
    )
  })()