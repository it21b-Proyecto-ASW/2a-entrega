const admin = require('./admin');
const { initializeApp } = require('firebase/app');
const { getAuth } = require('firebase/auth');
const { getStorage } = require('firebase/storage');
const { getFirestore } = require('firebase/firestore');

// Configuració de Firebase Client SDK
const firebaseConfig = {
  apiKey: "AIzaSyBVd3DFu7HL6FKup1y0x711CKBsrZCKWcg",
  authDomain: "issue-tracker-app-21.firebaseapp.com",
  projectId: "issue-tracker-app-21",
  storageBucket: "issue-tracker-app-21.firebasestorage.app",
  messagingSenderId: "582952539766",
  appId: "1:582952539766:web:59a2534f4914e394c7f157"
};

// Funció per inicialitzar Firebase
const initializeFirebase = () => {
  try {
    console.log('Inicialitzant Firebase...');
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    const storage = getStorage(app);
    const db = getFirestore(app);
    console.log('Firebase inicialitzat correctament');
    return { app, auth, storage, db };
  } catch (error) {
    console.error('Error inicialitzant Firebase:', error);
    throw error;
  }
};

// Inicialitzar Firebase Client
const { app, auth, storage, db } = initializeFirebase();

module.exports = {
  admin,
  auth,
  storage,
  db,
  initializeFirebase
}; 