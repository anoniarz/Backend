
function openLoginForm() {
    var overlay = document.getElementById("login-overlay");
    var loginForm = document.querySelector(".login-form");

    overlay.style.display = "block";
    loginForm.style.display = "block";
    document.body.style.filter = "blur(6px)";
}

function closeLoginForm() {
    var overlay = document.getElementById("login-overlay");
    var loginForm = document.querySelector(".login-form");

    overlay.style.display = "none";
    loginForm.style.display = "none";

    document.body.style.filter = "none";
}

function openRegisterForm() {
    var overlay = document.getElementById("register-overlay");
    var registerForm = document.querySelector(".register-form");

    overlay.style.display = "block";
    registerForm.style.display = "block";
    document.body.style.filter = "blur(6px)";
  }

  function closeRegisterForm() {
    var overlay = document.getElementById("register-overlay");
    var registerForm = document.querySelector(".register-form");

    overlay.style.display = "none";
    registerForm.style.display = "none";
    document.body.style.filter = "none";
  }

  
window.onclick = function(event) {
  var overlay = document.getElementById("login-overlay");
    if (event.target == overlay) {
      closeLoginForm();
    }
  }


var mes = document.getElementsByClassName("alert");
setTimeout(function(){
   if (mes && mes.length) {
       mes[0].classList.add('alert-hidden');
   }
}, 2000);
