const drop_btn = document.querySelector("ul");
document.querySelector(".drop-btn").onclick = function () {
  this.classList.toggle("active");
  drop_btn.classList.toggle("active");
};
