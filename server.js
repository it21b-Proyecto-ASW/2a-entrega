const express = require('express');
const cors = require('cors');
const multer = require('multer');
const admin = require('firebase-admin');
const path = require('path');
require('dotenv').config();

// Inicialitzar l'aplicació Express
const app = express();
const port = process.env.PORT || 3000;

// Configuració de Firebase Admin
const serviceAccount = {
    "type": "service_account",
    "project_id": process.env.FIREBASE_PROJECT_ID,
    "private_key_id": process.env.FIREBASE_ADMIN_PRIVATE_KEY_ID,
    "private_key": process.env.FIREBASE_ADMIN_PRIVATE_KEY.replace(/\\n/g, '\n'),
    "client_email": process.env.FIREBASE_ADMIN_CLIENT_EMAIL,
    "client_id": process.env.FIREBASE_ADMIN_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": process.env.FIREBASE_ADMIN_CLIENT_CERT_URL
};

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public', {
    setHeaders: (res, path) => {
        if (path.endsWith('.css')) {
            res.setHeader('Content-Type', 'text/css');
        } else if (path.endsWith('.js')) {
            res.setHeader('Content-Type', 'application/javascript');
        } else if (path.endsWith('.html')) {
            res.setHeader('Content-Type', 'text/html');
        }
    }
}));

// Configuració de Multer per a arxius
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

// Middleware d'autenticació
const authenticateToken = async (req, res, next) => {
    try {
        const authHeader = req.headers.authorization;
        if (!authHeader) {
            return res.status(401).json({ error: 'No token provided' });
        }

        const token = authHeader.split(' ')[1];
        const decodedToken = await admin.auth().verifyIdToken(token);
        req.user = decodedToken;
        next();
    } catch (error) {
        console.error('Error verifying token:', error);
        res.status(401).json({ error: 'Invalid token' });
    }
};

// Routes per a Issues
app.get('/api/issues', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const issuesSnapshot = await db.collection('issues').get();
        const issues = [];
        
        issuesSnapshot.forEach(doc => {
            issues.push({
                id: doc.id,
                ...doc.data()
            });
        });

        res.json(issues);
    } catch (error) {
        console.error('Error getting issues:', error);
        res.status(500).json({ error: 'Error getting issues' });
    }
});

app.post('/api/issues', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const issueData = {
            ...req.body,
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            createdBy: req.user.uid
        };

        const docRef = await db.collection('issues').add(issueData);
        res.status(201).json({ id: docRef.id, ...issueData });
    } catch (error) {
        console.error('Error creating issue:', error);
        res.status(500).json({ error: 'Error creating issue' });
    }
});

app.get('/api/issues/:id', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const doc = await db.collection('issues').doc(req.params.id).get();

        if (!doc.exists) {
            return res.status(404).json({ error: 'Issue not found' });
        }

        res.json({ id: doc.id, ...doc.data() });
    } catch (error) {
        console.error('Error getting issue:', error);
        res.status(500).json({ error: 'Error getting issue' });
    }
});

app.put('/api/issues/:id', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const docRef = db.collection('issues').doc(req.params.id);
        const doc = await docRef.get();

        if (!doc.exists) {
            return res.status(404).json({ error: 'Issue not found' });
        }

        await docRef.update({
            ...req.body,
            updatedAt: admin.firestore.FieldValue.serverTimestamp()
        });

        res.json({ id: doc.id, ...req.body });
    } catch (error) {
        console.error('Error updating issue:', error);
        res.status(500).json({ error: 'Error updating issue' });
    }
});

app.delete('/api/issues/:id', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const docRef = db.collection('issues').doc(req.params.id);
        const doc = await docRef.get();

        if (!doc.exists) {
            return res.status(404).json({ error: 'Issue not found' });
        }

        await docRef.delete();
        res.status(204).send();
    } catch (error) {
        console.error('Error deleting issue:', error);
        res.status(500).json({ error: 'Error deleting issue' });
    }
});

// Routes per a Comments
app.get('/api/issues/:issueId/comments', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const commentsSnapshot = await db
            .collection('issues')
            .doc(req.params.issueId)
            .collection('comments')
            .get();

        const comments = [];
        commentsSnapshot.forEach(doc => {
            comments.push({
                id: doc.id,
                ...doc.data()
            });
        });

        res.json(comments);
    } catch (error) {
        console.error('Error getting comments:', error);
        res.status(500).json({ error: 'Error getting comments' });
    }
});

app.post('/api/issues/:issueId/comments', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const commentData = {
            ...req.body,
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            createdBy: req.user.uid
        };

        const docRef = await db
            .collection('issues')
            .doc(req.params.issueId)
            .collection('comments')
            .add(commentData);

        res.status(201).json({ id: docRef.id, ...commentData });
    } catch (error) {
        console.error('Error creating comment:', error);
        res.status(500).json({ error: 'Error creating comment' });
    }
});

// Routes per a Attachments
app.get('/api/issues/:issueId/attachments', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const attachmentsSnapshot = await db
            .collection('issues')
            .doc(req.params.issueId)
            .collection('attachments')
            .get();

        const attachments = [];
        attachmentsSnapshot.forEach(doc => {
            attachments.push({
                id: doc.id,
                ...doc.data()
            });
        });

        res.json(attachments);
    } catch (error) {
        console.error('Error getting attachments:', error);
        res.status(500).json({ error: 'Error getting attachments' });
    }
});

app.post('/api/issues/:issueId/attachments', authenticateToken, upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const db = admin.firestore();
        const attachmentData = {
            name: req.file.originalname,
            path: req.file.path,
            size: req.file.size,
            type: req.file.mimetype,
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            createdBy: req.user.uid
        };

        const docRef = await db
            .collection('issues')
            .doc(req.params.issueId)
            .collection('attachments')
            .add(attachmentData);

        res.status(201).json({ id: docRef.id, ...attachmentData });
    } catch (error) {
        console.error('Error uploading attachment:', error);
        res.status(500).json({ error: 'Error uploading attachment' });
    }
});

app.delete('/api/issues/:issueId/attachments/:attachmentId', authenticateToken, async (req, res) => {
    try {
        const db = admin.firestore();
        const docRef = db
            .collection('issues')
            .doc(req.params.issueId)
            .collection('attachments')
            .doc(req.params.attachmentId);

        const doc = await docRef.get();
        if (!doc.exists) {
            return res.status(404).json({ error: 'Attachment not found' });
        }

        await docRef.delete();
        res.status(204).send();
    } catch (error) {
        console.error('Error deleting attachment:', error);
        res.status(500).json({ error: 'Error deleting attachment' });
    }
});

// Ruta per a qualsevol altra petició
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'issues.html'));
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
}); 