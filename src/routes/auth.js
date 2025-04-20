const express = require('express');
const router = express.Router();
const { signInWithGoogle, signInWithEmail, signUpWithEmail } = require('../config/auth');
const { admin } = require('../config/firebase');

// Ruta per iniciar sessió amb Google
router.post('/google', async (req, res) => {
  try {
    const user = await signInWithGoogle();
    res.json({ user });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Ruta per iniciar sessió amb email/password
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await signInWithEmail(email, password);
    res.json({ user });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Ruta per registrar-se amb email/password
router.post('/register', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await signUpWithEmail(email, password);
    res.json({ user });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = router; 