// Configuració de Firebase
const firebaseConfig = {
    apiKey: "AIzaSyBVd3DFu7HL6FKup1y0x711CKBsrZCKWcg",
    authDomain: "issue-tracker-app-21.firebaseapp.com",
    projectId: "issue-tracker-app-21",
    storageBucket: "issue-tracker-app-21.appspot.com",
    messagingSenderId: "582952539766",
    appId: "1:582952539766:web:59a2534f4914e394c7f157"
};

// Carregar la navbar
document.addEventListener('DOMContentLoaded', () => {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) return;

    fetch('/navbar.html')
        .then(response => response.text())
        .then(html => {
            navbarContainer.innerHTML = html;
            initializeNavbar();
        })
        .catch(error => console.error('Error carregant la navbar:', error));
});

// Inicialitzar la navbar
function initializeNavbar() {
    // Inicialitzar Firebase
    let app;
    let auth;
    let db;

    try {
        if (!app) {
            app = firebase.initializeApp(firebaseConfig);
        }

        if (!auth) {
            auth = firebase.auth();
        }

        if (!db) {
            db = firebase.firestore();
        }

        // Comprovar si l'usuari està autenticat
        auth.onAuthStateChanged(user => {
            const loginLink = document.getElementById('login-link');
            const profileLink = document.getElementById('profile-link');
            const logoutLink = document.getElementById('logout-link');

            if (user) {
                // Usuari autenticat
                if (loginLink) loginLink.style.display = 'none';
                if (profileLink) profileLink.style.display = 'block';
                if (logoutLink) logoutLink.style.display = 'block';
            } else {
                // Usuari no autenticat
                if (loginLink) loginLink.style.display = 'block';
                if (profileLink) profileLink.style.display = 'none';
                if (logoutLink) logoutLink.style.display = 'none';
            }
        });

        // Configurar l'esdeveniment de logout
        const logoutLink = document.getElementById('logout-link');
        if (logoutLink) {
            logoutLink.addEventListener('click', async (e) => {
                e.preventDefault();
                try {
                    await auth.signOut();
                    window.location.href = '/auth.html';
                } catch (error) {
                    console.error('Error en el logout:', error);
                }
            });
        }
    } catch (error) {
        console.error('Error inicialitzant Firebase:', error);
    }
} 