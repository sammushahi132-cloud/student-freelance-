/**
 * Student Freelance Marketplace - Basic Frontend JavaScript
 * Simple, beginner-friendly DOM manipulation and confirmation handlers.
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log("Student Freelance Marketplace script loaded successfully.");

    // -------------------------------------------------------------------------
    // 1. Show / Hide Password Functionality
    // -------------------------------------------------------------------------
    const togglePasswordButtons = document.querySelectorAll('.toggle-password-btn');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function () {
            const targetInputId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetInputId);
            const icon = this.querySelector('i');

            if (targetInput) {
                if (targetInput.type === 'password') {
                    targetInput.type = 'text';
                    if (icon) {
                        icon.classList.remove('bi-eye');
                        icon.classList.add('bi-eye-slash');
                    }
                    this.setAttribute('title', 'Hide password');
                } else {
                    targetInput.type = 'password';
                    if (icon) {
                        icon.classList.remove('bi-eye-slash');
                        icon.classList.add('bi-eye');
                    }
                    this.setAttribute('title', 'Show password');
                }
            }
        });
    });

    // -------------------------------------------------------------------------
    // 2. Project Deletion Confirmation
    // -------------------------------------------------------------------------
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const projectTitle = this.getAttribute('data-project-title') || 'this project';
            const confirmed = window.confirm(`Are you sure you want to permanently delete "${projectTitle}"?\nThis action cannot be undone.`);
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // -------------------------------------------------------------------------
    // 3. Proposal Acceptance Confirmation
    // -------------------------------------------------------------------------
    const acceptButtons = document.querySelectorAll('.btn-confirm-accept');
    acceptButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const studentName = this.getAttribute('data-student-name') || 'this student';
            const confirmed = window.confirm(`Accept proposal from ${studentName}?\nThis will mark the project as Assigned and reject other pending proposals.`);
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // -------------------------------------------------------------------------
    // 4. Basic Frontend Form Validation
    // -------------------------------------------------------------------------
    const registrationForm = document.querySelector('form#registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function (event) {
            const pass = document.getElementById('reg_password');
            const confirmPass = document.getElementById('reg_confirm_password');

            if (pass && confirmPass && pass.value !== confirmPass.value) {
                alert("Passwords do not match! Please verify your password.");
                confirmPass.focus();
                event.preventDefault();
                return false;
            }

            if (pass && pass.value.length < 6) {
                alert("Password should be at least 6 characters long.");
                pass.focus();
                event.preventDefault();
                return false;
            }
        });
    }

    // Budget and Proposed Amount positive numbers check
    const amountInputs = document.querySelectorAll('input[type="number"][min="1"]');
    amountInputs.forEach(input => {
        input.addEventListener('change', function () {
            if (parseFloat(this.value) <= 0) {
                alert("Value must be greater than zero.");
                this.value = '1';
            }
        });
    });

    // -------------------------------------------------------------------------
    // 5. Auto-dismiss Alert Messages after 5 seconds
    // -------------------------------------------------------------------------
    const alertElements = document.querySelectorAll('.alert-dismissible');
    alertElements.forEach(alert => {
        setTimeout(() => {
            // Check if Bootstrap's Alert instance exists
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                // Fallback fade out
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });
});

