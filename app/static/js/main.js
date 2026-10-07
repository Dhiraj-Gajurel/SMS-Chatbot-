// XYZ SCHOOL AND COLLEGE - MAIN INTERACTIVE JS (SLICK SLIDER INTEGRATION)
$(document.body).ready(function() {
    // 1. Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }

    // 2. Slick Slider Initialization for Hero Section (No Dots, Auto Slider, Pause on Hover)
    if ($('.hero-slick-slider').length) {
        $('.hero-slick-slider').slick({
            dots: false, // Dots removed as requested
            infinite: true,
            speed: 800,
            fade: true,
            cssEase: 'cubic-bezier(0.16, 1, 0.3, 1)',
            autoplay: true, // Auto slider enabled
            autoplaySpeed: 4000,
            arrows: true,
            prevArrow: '<button type="button" class="slick-prev" aria-label="Previous Slide"><i class="fas fa-chevron-left"></i></button>',
            nextArrow: '<button type="button" class="slick-next" aria-label="Next Slide"><i class="fas fa-chevron-right"></i></button>',
            pauseOnHover: true, // Pause on hover enabled
            pauseOnFocus: true,
            pauseOnDotsHover: true,
            adaptiveHeight: false
        });
    }

    // 3. Category Filtering (Gallery & Notices)
    const filterButtons = document.querySelectorAll('.filter-btn');
    const filterItems = document.querySelectorAll('.filterable-item');

    if (filterButtons.length > 0 && filterItems.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                filterButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const filterValue = this.getAttribute('data-filter');
                filterItems.forEach(item => {
                    if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        });
    }

    // 4. Auto-hide flash alerts
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.5s ease';
                setTimeout(() => alert.remove(), 500);
            });
        }, 5000);
    }
});
