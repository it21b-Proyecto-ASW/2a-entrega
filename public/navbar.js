// Carregar la navbar
document.addEventListener('DOMContentLoaded', () => {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) return;

    fetch('/navbar.html')
        .then(response => response.text())
        .then(html => {
            navbarContainer.innerHTML = html;
        })
        .catch(error => console.error('Error carregant la navbar:', error));
}); 