document.addEventListener("DOMContentLoaded", function () {
    // Selecting the header element
    const header = document.querySelector("header");

    // Change header background color when it's clicked
    header.addEventListener("click", function () {
        //header.style.backgroundColor = white();
    });

    // Function to generate a random color
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Simple console log
    console.log("Website loaded successfully!");
});