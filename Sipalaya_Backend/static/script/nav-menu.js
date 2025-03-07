const toggleButton = document.querySelector('.toggle-button');
const closeButton = document.querySelector('.close-button');
const mobileNav = document.querySelector('nav ul');
const navItem = document.querySelectorAll('li a');

// Function to update menu display based on screen size
const updateMenuDisplay = () => {
    if (window.innerWidth > 876) {
        mobileNav.style.display = 'flex'; // Show menu in desktop view
        closeButton.style.display = 'none'; // Hide close button
    } else {
        mobileNav.style.display = 'none'; // Hide menu in mobile view
    }
};

// Run the function on page load
document.addEventListener("DOMContentLoaded", updateMenuDisplay);

// Run the function when resizing the window
window.addEventListener("resize", updateMenuDisplay);

// Show mobile menu when toggle button is clicked
const Display = () => {
    mobileNav.style.display = 'block';
    closeButton.style.display = 'block';
};

// Hide mobile menu
const Close = () => {
    mobileNav.style.display = 'none';
    closeButton.style.display = 'none';
};

toggleButton.addEventListener('click', Display);
closeButton.addEventListener('click', Close);

// Close menu when clicking a nav item in mobile view
navItem.forEach(item => {
    item.addEventListener('click', () => {
        if (window.innerWidth < 876) Close();
    });
});
