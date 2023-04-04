
function openLoginForm() {
    var overlay = document.getElementById("login-overlay");
    overlay.style.display = "block";

    document.body.classList.add("blur");
  }
  
  function closeLoginForm() {
    var overlay = document.getElementById("login-overlay");
    overlay.style.display = "none";
    
    document.body.classList.remove("blur");
  }

function openRegisterForm() {
    var overlay = document.getElementById("register-overlay");
    overlay.style.display = "block";

    document.body.classList.add("blur");
  }

function closeRegisterForm() {
    var overlay = document.getElementById("register-overlay");
    overlay.style.display = "none";
    
    document.body.classList.remove("blur");
  }

function sign_up() {
    closeLoginForm();
    document.body.classList.add("blur");
    setTimeout(openRegisterForm, 300);
  }

function log_in() {
    closeRegisterForm();
    document.body.classList.add("blur");
    setTimeout(openLoginForm, 300);
  }

window.onclick = function(event) {
    var overlay = document.getElementById("login-overlay");
    if (event.target == overlay) {
        closeLoginForm();
    }
}


var mes = document.getElementsByClassName("alert");
setTimeout(function() {
    if (mes && mes.length) {
        mes[0].classList.add('alert-hidden');
    }
}, 2000);