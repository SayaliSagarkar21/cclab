// Script for enhancing the weather app UI

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in effect to weather cards
    const weatherCard = document.querySelector('.weather-card');
    if (weatherCard) {
        weatherCard.style.opacity = '0';
        setTimeout(() => {
            weatherCard.style.transition = 'opacity 0.5s ease-in';
            weatherCard.style.opacity = '1';
        }, 100);
    }

    // Add animations to the weather icon
    const weatherIcon = document.querySelector('.weather-icon img');
    if (weatherIcon) {
        weatherIcon.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        weatherIcon.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    }

    // Enhance form submissions with validation
    const weatherForm = document.querySelector('form[action*="weather"]');
    if (weatherForm) {
        weatherForm.addEventListener('submit', function(e) {
            const cityInput = this.querySelector('input[name="city"]');
            if (cityInput.value.trim() === '') {
                e.preventDefault();
                cityInput.classList.add('is-invalid');
                
                // Create error message if it doesn't exist
                let errorMsg = cityInput.nextElementSibling;
                if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg = document.createElement('div');
                    errorMsg.classList.add('invalid-feedback');
                    errorMsg.textContent = 'Please enter a city name';
                    cityInput.parentNode.insertBefore(errorMsg, cityInput.nextSibling);
                }
            }
        });
    }
});