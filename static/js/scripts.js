// popup message
document.addEventListener("DOMContentLoaded", () => {
    // Read message passed from server via <body data-message="...">
    const message = document.body.dataset.message;

    // Grab elements
    const popup = document.getElementById("custom-popup");
    const popupMessage = document.getElementById("popup-message");

    // Safety checks
    if (!popup || !popupMessage) {
        console.warn("Popup elements not found. Check #custom-popup and #popup-message.");
        return;
    }

    // Show the popup with text
    function showPopup(text) {
        popupMessage.textContent = text;
        popup.classList.add("show");      // fade-in
        popup.classList.remove("hidden"); // legacy compatibility if you still have .hidden
        // Auto-close after 3 seconds
        setTimeout(hidePopup, 1500);
    }

    // Hide the popup
    function hidePopup() {
        popup.classList.remove("show");   // fade-out
        popup.classList.add("hidden");    // harmless if .hidden is not defined
    }

    // Close when clicking the backdrop (but not when clicking the content)
    popup.addEventListener("click", (e) => {
        // Use currentTarget to ensure we only react to backdrop clicks
        if (e.target === e.currentTarget) hidePopup();
    });

    // Trigger on load if message exists
    if (message && message.trim() !== "" && message !== "None") {
        showPopup(message);
    }
});


// Get elements from form with password
const passwordField = document.getElementById("password");
const confirmPasswordField = document.getElementById("confirm_password");
const passwordError = document.getElementById("passwordError");
const confirmPasswordError = document.getElementById("confirmPasswordError");
const form = document.getElementById("passwordForm");

// Check if passwords match
function checkPasswordsMatch() {
    if (passwordField.value !== confirmPasswordField.value) {
        confirmPasswordError.textContent = "Passwords do not match!";
        return false;
    } else {
        confirmPasswordError.textContent = "";
        return true;
    }
}

// Check password length
function checkPasswordLength(minLength = 6) {
    if (passwordField.value.length < minLength) {
        passwordError.textContent = `Password must be at least ${minLength} characters long!`;
        return false;
    } else {
        passwordError.textContent = "";
        return true;
    }
}

// Validate on form submit
form.addEventListener("submit", function(event) {
    const isLengthValid = checkPasswordLength();
    const isMatch = checkPasswordsMatch();

    if (!isLengthValid || !isMatch) {
        event.preventDefault(); // stop submission if validation fails
    }
});

// Live validation while typing
passwordField.addEventListener("input", () => {
    checkPasswordLength();
    checkPasswordsMatch();
});

confirmPasswordField.addEventListener("input", checkPasswordsMatch);
