// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Course search functionality
    const searchInput = document.getElementById('courseSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const courseCards = document.querySelectorAll('.course-card');
            
            courseCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Course filter functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.dataset.filter;
                const courseCards = document.querySelectorAll('.course-card');
                
                courseCards.forEach(card => {
                    if (filter === 'all' || card.dataset.category === filter) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
                
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }

    // Course rating functionality
    const ratingInputs = document.querySelectorAll('.rating-input');
    if (ratingInputs.length > 0) {
        ratingInputs.forEach(input => {
            input.addEventListener('change', function() {
                const rating = this.value;
                const stars = this.parentElement.querySelectorAll('.star');
                
                stars.forEach((star, index) => {
                    if (index < rating) {
                        star.classList.add('active');
                    } else {
                        star.classList.remove('active');
                    }
                });
            });
        });
    }

    // Course enrollment functionality
    const enrollButtons = document.querySelectorAll('.enroll-btn');
    if (enrollButtons.length > 0) {
        enrollButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const courseId = this.dataset.courseId;
                
                // Show loading state
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enrolling...';
                this.disabled = true;
                
                // Simulate API call
                setTimeout(() => {
                    // Redirect to payment page
                    window.location.href = `/courses/${courseId}/enroll/`;
                }, 1000);
            });
        });
    }

    // Course progress tracking
    const progressBars = document.querySelectorAll('.progress-bar');
    if (progressBars.length > 0) {
        progressBars.forEach(bar => {
            const progress = bar.dataset.progress;
            bar.style.width = `${progress}%`;
            bar.setAttribute('aria-valuenow', progress);
        });
    }

    // Course video player
    const videoPlayer = document.getElementById('courseVideo');
    if (videoPlayer) {
        // Initialize video player with custom controls
        videoPlayer.addEventListener('play', function() {
            // Track video progress
            setInterval(() => {
                const progress = (videoPlayer.currentTime / videoPlayer.duration) * 100;
                const progressBar = document.querySelector('.video-progress-bar');
                if (progressBar) {
                    progressBar.style.width = `${progress}%`;
                }
            }, 1000);
        });
    }

    // Course discussion forum
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const commentText = this.querySelector('textarea').value;
            
            if (commentText.trim()) {
                // Add comment to the list
                const commentsList = document.querySelector('.comments-list');
                const newComment = document.createElement('div');
                newComment.className = 'comment';
                newComment.innerHTML = `
                    <div class="comment-header">
                        <img src="/static/images/default-avatar.png" alt="User Avatar" class="avatar">
                        <div class="comment-info">
                            <h6>Current User</h6>
                            <small>Just now</small>
                        </div>
                    </div>
                    <div class="comment-body">
                        ${commentText}
                    </div>
                `;
                commentsList.prepend(newComment);
                
                // Clear form
                this.reset();
            }
        });
    }

    // Course certificate generation
    const certificateButton = document.getElementById('generateCertificate');
    if (certificateButton) {
        certificateButton.addEventListener('click', function() {
            // Show loading state
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
            this.disabled = true;
            
            // Simulate certificate generation
            setTimeout(() => {
                // Show success message
                const alert = document.createElement('div');
                alert.className = 'alert alert-success';
                alert.innerHTML = 'Certificate generated successfully! <a href="#" class="alert-link">Download</a>';
                this.parentElement.appendChild(alert);
                
                // Reset button
                this.innerHTML = 'Generate Certificate';
                this.disabled = false;
            }, 2000);
        });
    }

    // Course feedback form
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const feedback = this.querySelector('textarea').value;
            
            if (feedback.trim()) {
                // Show success message
                const alert = document.createElement('div');
                alert.className = 'alert alert-success';
                alert.innerHTML = 'Thank you for your feedback!';
                this.parentElement.appendChild(alert);
                
                // Clear form
                this.reset();
            }
        });
    }
});

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}); 