const { admin } = require('../config/firebase');

const adminMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const token = authHeader.split('Bearer ')[1];
    const decodedToken = await admin.auth().verifyIdToken(token);
    
    // Comprovar si l'usuari té el rol d'admin
    const user = await admin.auth().getUser(decodedToken.uid);
    const isAdmin = user.customClaims && user.customClaims.admin === true;
    
    if (!isAdmin) {
      return res.status(403).json({ error: 'Access denied. Admin privileges required.' });
    }
    
    req.user = decodedToken;
    next();
  } catch (error) {
    console.error('Error verifying admin token:', error);
    return res.status(401).json({ error: 'Invalid token' });
  }
};

module.exports = adminMiddleware; 