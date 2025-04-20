// Configuració de Firebase
const firebaseConfig = {
    apiKey: "AIzaSyBVd3DFu7HL6FKup1y0x711CKBsrZCKWcg",
    authDomain: "issue-tracker-app-21.firebaseapp.com",
    projectId: "issue-tracker-app-21",
    storageBucket: "issue-tracker-app-21.appspot.com",
    messagingSenderId: "582952539766",
    appId: "1:582952539766:web:59a2534f4914e394c7f157"
};

// Inicialitzar Firebase
let app;
let auth;

async function initializeFirebase() {
    try {
        if (!app) {
            app = firebase.initializeApp(firebaseConfig);
        }

        if (!auth) {
            auth = firebase.auth();
        }

        // Esperar a que l'autenticació estigui llesta
        const user = await new Promise((resolve, reject) => {
            const authTimeout = setTimeout(() => {
                reject(new Error('Timeout esperant autenticació'));
            }, 10000);

            const unsubscribe = auth.onAuthStateChanged(user => {
                clearTimeout(authTimeout);
                unsubscribe();
                resolve(user);
            });
        });

        if (!user) {
            window.location.href = '/index.html';
            return;
        }

        // Mostrar informació de l'usuari
        document.getElementById('user-info').textContent = user.email;
    } catch (error) {
        console.error('Error inicialitzant Firebase:', error);
        window.location.href = '/index.html';
    }
}

// Tancar sessió
document.getElementById('logout-button').addEventListener('click', async () => {
    try {
        await auth.signOut();
        window.location.href = '/index.html';
    } catch (error) {
        console.error('Error tancant sessió:', error);
    }
});

// Inicialitzar quan es carrega la pàgina
window.addEventListener('load', initializeFirebase); 