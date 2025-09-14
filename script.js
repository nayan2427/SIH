// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    // Load statistics
    loadStats();
    
    // Initialize smooth scrolling
    initSmoothScrolling();
    
    // Initialize form handling
    initFormHandling();
});

// Load platform statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        // Animate counter numbers
        animateCounter('total-internships', stats.total_internships);
        animateCounter('trust-internships', stats.trust_internships);
        animateCounter('government-internships', stats.government_internships);
        animateCounter('private-internships', stats.private_internships);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Animate counter numbers
function animateCounter(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let currentValue = 0;
    const increment = targetValue / 50;
    const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= targetValue) {
            currentValue = targetValue;
            clearInterval(timer);
        }
        element.textContent = Math.floor(currentValue);
    }, 30);
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 70; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Form handling and validation
function initFormHandling() {
    // Contact form
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
    
    // Registration form
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegistrationForm);
    }
    
    // Login form
    const loginForm = document.querySelector('form[action*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginForm);
    }
    
    // Profile update form
    const profileForm = document.querySelector('form[action*="update_profile"]');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileUpdateForm);
    }
    
    // Aadhar verification form
    const aadharForm = document.querySelector('form[action*="verify_aadhar"]');
    if (aadharForm) {
        aadharForm.addEventListener('submit', handleAadharVerification);
    }
    
    // Application form
    const applicationForm = document.querySelector('form[action*="apply"]');
    if (applicationForm) {
        applicationForm.addEventListener('submit', handleApplicationForm);
    }
}

// Handle contact form submission
function handleContactForm(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');
    
    // Basic validation
    if (!name || !email || !message) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showAlert('Please enter a valid email address', 'error');
        return;
    }
    
    // Simulate form submission
    showLoading(e.target.querySelector('button[type="submit"]'));
    
    setTimeout(() => {
        hideLoading(e.target.querySelector('button[type="submit"]'));
        showAlert('Thank you for your message! We\'ll get back to you soon.', 'success');
        e.target.reset();
    }, 2000);
}

// Handle registration form
function handleRegistrationForm(e) {
    const formData = new FormData(e.target);
    const email = formData.get('email');
    const mobile = formData.get('mobile');
    const graduationYear = parseInt(formData.get('graduation_year'));
    
    // Validation
    if (!isValidEmail(email)) {
        e.preventDefault();
        showAlert('Please enter a valid email address', 'error');
        return;
    }
    
    if (!isValidMobile(mobile)) {
        e.preventDefault();
        showAlert('Please enter a valid mobile number', 'error');
        return;
    }
    
    if (graduationYear < 2020 || graduationYear > 2030) {
        e.preventDefault();
        showAlert('Please enter a valid graduation year', 'error');
        return;
    }
}

// Handle login form
function handleLoginForm(e) {
    const formData = new FormData(e.target);
    const email = formData.get('email');
    
    if (!isValidEmail(email)) {
        e.preventDefault();
        showAlert('Please enter a valid email address', 'error');
        return;
    }
}

// Handle profile update form
function handleProfileUpdateForm(e) {
    const formData = new FormData(e.target);
    const email = formData.get('email');
    const mobile = formData.get('mobile');
    const graduationYear = parseInt(formData.get('graduation_year'));
    
    if (email && !isValidEmail(email)) {
        e.preventDefault();
        showAlert('Please enter a valid email address', 'error');
        return;
    }
    
    if (mobile && !isValidMobile(mobile)) {
        e.preventDefault();
        showAlert('Please enter a valid mobile number', 'error');
        return;
    }
    
    if (graduationYear && (graduationYear < 2020 || graduationYear > 2030)) {
        e.preventDefault();
        showAlert('Please enter a valid graduation year', 'error');
        return;
    }
}

// Handle Aadhar verification
function handleAadharVerification(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const aadharNumber = formData.get('aadhar_number');
    
    if (!isValidAadhar(aadharNumber)) {
        showAlert('Please enter a valid 12-digit Aadhar number', 'error');
        return;
    }
    
    // Simulate DigiLocker verification
    showLoading(e.target.querySelector('button[type="submit"]'));
    
    setTimeout(() => {
        hideLoading(e.target.querySelector('button[type="submit"]'));
        showAlert('Aadhar verification successful! Your profile is now verified.', 'success');
        // Submit the form
        e.target.submit();
    }, 3000);
}

// Handle application form
function handleApplicationForm(e) {
    const formData = new FormData(e.target);
    const coverLetter = formData.get('cover_letter');
    
    if (coverLetter && coverLetter.length < 50) {
        e.preventDefault();
        showAlert('Cover letter should be at least 50 characters long', 'error');
        return;
    }
    
    showLoading(e.target.querySelector('button[type="submit"]'));
}

// Validation functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidMobile(mobile) {
    const mobileRegex = /^[6-9]\d{9}$/;
    return mobileRegex.test(mobile);
}

function isValidAadhar(aadhar) {
    const aadharRegex = /^\d{12}$/;
    return aadharRegex.test(aadhar);
}

// Show loading state
function showLoading(button) {
    if (!button) return;
    
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Processing...';
}

// Hide loading state
function hideLoading(button) {
    if (!button) return;
    
    button.disabled = false;
    button.innerHTML = button.getAttribute('data-original-text') || 'Submit';
}

// Show alert message
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    // Insert at the top of the page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alert, container.firstChild);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Internship filtering and search
function initInternshipFilters() {
    const searchInput = document.getElementById('search-input');
    const companyTypeFilter = document.getElementById('company-type-filter');
    const categoryFilter = document.getElementById('category-filter');
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterInternships, 300));
    }
    
    if (companyTypeFilter) {
        companyTypeFilter.addEventListener('change', filterInternships);
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterInternships);
    }
}

// Filter internships based on search and filters
function filterInternships() {
    const searchTerm = document.getElementById('search-input')?.value.toLowerCase() || '';
    const companyType = document.getElementById('company-type-filter')?.value || 'all';
    const category = document.getElementById('category-filter')?.value || 'all';
    
    const internshipCards = document.querySelectorAll('.internship-card');
    
    internshipCards.forEach(card => {
        const title = card.querySelector('.internship-title')?.textContent.toLowerCase() || '';
        const company = card.querySelector('.company-name')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.internship-description')?.textContent.toLowerCase() || '';
        const cardCompanyType = card.querySelector('.company-type')?.textContent.toLowerCase() || '';
        const cardCategory = card.querySelector('.internship-category')?.textContent.toLowerCase() || '';
        
        const matchesSearch = !searchTerm || 
            title.includes(searchTerm) || 
            company.includes(searchTerm) || 
            description.includes(searchTerm);
        
        const matchesCompanyType = companyType === 'all' || cardCompanyType.includes(companyType);
        const matchesCategory = category === 'all' || cardCategory.includes(category);
        
        if (matchesSearch && matchesCompanyType && matchesCategory) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Debounce function for search input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize internship filters when page loads
document.addEventListener('DOMContentLoaded', function() {
    initInternshipFilters();
});

// Profile image upload (if implemented)
function handleProfileImageUpload(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const profileAvatar = document.querySelector('.profile-avatar');
            if (profileAvatar) {
                profileAvatar.style.backgroundImage = `url(${e.target.result})`;
                profileAvatar.style.backgroundSize = 'cover';
                profileAvatar.style.backgroundPosition = 'center';
            }
        };
        reader.readAsDataURL(file);
    }
}

// Application status tracking
function trackApplicationStatus(applicationId) {
    // This would typically make an API call to check status
    console.log('Tracking application status for:', applicationId);
}

// Bookmark functionality (if implemented)
function toggleBookmark(internshipId) {
    const bookmarkBtn = document.querySelector(`[data-internship-id="${internshipId}"]`);
    if (bookmarkBtn) {
        const isBookmarked = bookmarkBtn.classList.contains('bookmarked');
        
        if (isBookmarked) {
            bookmarkBtn.classList.remove('bookmarked');
            bookmarkBtn.innerHTML = '<i class="far fa-bookmark"></i> Save';
        } else {
            bookmarkBtn.classList.add('bookmarked');
            bookmarkBtn.innerHTML = '<i class="fas fa-bookmark"></i> Saved';
        }
        
        // Here you would typically make an API call to save/remove bookmark
        console.log('Bookmark toggled for internship:', internshipId);
    }
}

// Share functionality
function shareInternship(internshipId, title) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: `Check out this internship opportunity: ${title}`,
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            showAlert('Link copied to clipboard!', 'success');
        });
    }
}

// Initialize tooltips (if using a tooltip library)
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Initialize tooltips when page loads
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
});

// Lazy loading for images (if implemented)
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading when page loads
document.addEventListener('DOMContentLoaded', function() {
    initLazyLoading();
});

// Export functions for use in other scripts
window.InternshipHub = {
    showAlert,
    showLoading,
    hideLoading,
    toggleBookmark,
    shareInternship,
    trackApplicationStatus
};
