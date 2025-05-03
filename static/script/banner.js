document.addEventListener("DOMContentLoaded", function () {
    let slides = document.querySelectorAll(".slide");
    let currentIndex = 0;

    function changeSlide() {
        let prevIndex = currentIndex;
        currentIndex = (currentIndex + 1) % slides.length;

        slides[prevIndex].classList.remove("active");
        slides[prevIndex].classList.add("prev"); // Move out of view
        slides[currentIndex].classList.add("active");

        // Remove "prev" class after animation to prevent stacking issues
        setTimeout(() => slides[prevIndex].classList.remove("prev"), 1500);
    }

    slides[currentIndex].classList.add("active"); // Show the first slide
    setInterval(changeSlide, 3000); // Change every 3 seconds
});
