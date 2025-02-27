document.addEventListener("DOMContentLoaded", function () {
    let slides = document.querySelectorAll(".slide");
    let index = 0;

    function showSlide(i) {
        slides.forEach(slide => slide.style.display = "none");
        slides[i].style.display = "block";
    }

    function nextSlide() {
        index = (index + 1) % slides.length;
        showSlide(index);
    }

    showSlide(index);
    setInterval(nextSlide, 3000);  // Rotate every 3 seconds
});
