const { auth } = require('./firebase');
const { GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword } = require('firebase/auth');

// Autenticació amb Google
const signInWithGoogle = async () => {
  try {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    return result.user;
  } catch (error) {
    console.error('Error en l\'autenticació amb Google:', error);
    throw error;
  }
};

// Autenticació amb email i contrasenya
const signInWithEmail = async (email, password) => {
  try {
    const result = await signInWithEmailAndPassword(auth, email, password);
    return result.user;
  } catch (error) {
    console.error('Error en l\'autenticació amb email:', error);
    throw error;
  }
};

// Registre amb email i contrasenya
const signUpWithEmail = async (email, password) => {
  try {
    const result = await createUserWithEmailAndPassword(auth, email, password);
    return result.user;
  } catch (error) {
    console.error('Error en el registre amb email:', error);
    throw error;
  }
};

module.exports = {
  signInWithGoogle,
  signInWithEmail,
  signUpWithEmail
}; 