document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.querySelector('button');
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function() {
        searchButton.disabled = true;
        searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
    });
});