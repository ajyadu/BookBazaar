document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        document.querySelectorAll(".alert").forEach(function (alert) {
            alert.style.transition = "opacity .5s";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        });
    }, 4000);
});
