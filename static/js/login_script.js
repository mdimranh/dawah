var animation = bodymovin.loadAnimation({
  container: document.getElementById("anim"),
  renderer: "svg",
  loop: true,
  autoplay: true,
  path: "../../static/json/login.json",
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
