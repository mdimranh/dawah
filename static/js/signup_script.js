var animation = bodymovin.loadAnimation({
  container: document.getElementById("anim"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "../../static/json/signup.json",
});

function password_show_hide() {
  var x = document.getElementById("password");
  var show_eye = document.getElementById("show-eye");
  var hide_eye = document.getElementById("hide-eye");
  hide_eye.classList.remove("d-none");
  if (x.type === "password") {
    x.type = "text";
    show_eye.style.display = "none";
    hide_eye.style.display = "block";
  } else {
    x.type = "password";
    show_eye.style.display = "block";
    hide_eye.style.display = "none";
  }
}

function cpassword_show_hide() {
  var y = document.getElementById("cpassword");
  var cshow_eye = document.getElementById("cshow-eye");
  var chide_eye = document.getElementById("chide-eye");
  chide_eye.classList.remove("d-none");
  if (y.type === "password") {
    y.type = "text";
    cshow_eye.style.display = "none";
    chide_eye.style.display = "block";
  } else {
    y.type = "password";
    cshow_eye.style.display = "block";
    chide_eye.style.display = "none";
  }
}
