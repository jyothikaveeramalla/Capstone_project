// Form submissions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Skip auth forms (signin, signup)
            if (form.id === 'signinForm' || form.id === 'signupForm') {
                return;
            }

            e.preventDefault();

            // Check if user is logged in for forms that require authentication
            if (form.classList.contains('requires-auth')) {
                if (!auth.isLoggedIn()) {
                    auth.setRedirectUrl(window.location.href);
                    window.location.href = 'signin.html';
                    return;
                }
            }

            alert('Thank you for your interest! We\'ll get back to you soon.');
        });
    });

    // Add smooth scrolling animation on page load
    document.body.style.animation = 'fadeInUp 0.8s ease';
    
    // Initialize stats animation if on home page
    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        animateStatsOnScroll();
    }
    
    // Add hover effects for product cards
    addProductCardEffects();
});

// Stats counter animation
function animateStats() {
    const statsNumbers = document.querySelectorAll('.stat-item h3');
    statsNumbers.forEach(stat => {
        const target = parseInt(stat.textContent.replace(/[^\d]/g, ''));
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                clearInterval(timer);
                current = target;
            }
            const suffix = stat.textContent.includes('+') ? '+' : 
                          stat.textContent.includes('%') ? '%' : '';
            stat.textContent = Math.floor(current) + suffix;
        }, 20);
    });
}

// Trigger stats animation when stats section is visible
function animateStatsOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStats();
                observer.unobserve(entry.target); // Only animate once
            }
        });
    });

    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        observer.observe(statsSection);
    }
}

// Add hover effects for product cards
function addProductCardEffects() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
        });
    });
}

// Mobile menu toggle functionality
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
}

// Add active navigation highlighting
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.style.color = '#97d69b';
        }
    });
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Form validation enhancements
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            field.style.borderColor = '#4a8f4e';
        }
    });
    
    return isValid;
}

// Add loading states to forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                if (validateForm(form)) {
                    submitButton.textContent = 'Processing...';
                    submitButton.disabled = true;
                    
                    // Simulate processing time
                    setTimeout(() => {
                        submitButton.textContent = 'Success!';
                        setTimeout(() => {
                            submitButton.textContent = submitButton.getAttribute('data-original-text') || 'Submit';
                            submitButton.disabled = false;
                            form.reset();
                        }, 2000);
                    }, 1500);
                }
            });
            
            // Store original button text
            submitButton.setAttribute('data-original-text', submitButton.textContent);
        }
    });
});

// Add scroll-to-top functionality
document.addEventListener('DOMContentLoaded', function() {
    // Create scroll to top button
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '↑';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border: none;
        border-radius: 50%;
        background: #2c5f2d;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1000;
    `;
    
    document.body.appendChild(scrollTopBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.opacity = '1';
        } else {
            scrollTopBtn.style.opacity = '0';
        }
    });
    
    // Scroll to top when clicked
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// Add intersection observer for animations
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease forwards';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.feature-card, .product-card, .form-container');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
});