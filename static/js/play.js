function expandTextarea(id) {
  document.getElementById(id).addEventListener(
    "keyup",
    function () {
      this.style.overflow = "hidden";
      this.style.height = 0;
      this.style.height = this.scrollHeight + "px";
    },
    false
  );
}

expandTextarea("txtarea");

function eraseText() {
  document.getElementById("txtarea").value = "";
  document.getElementById("txtarea").style.height = 0;
}
