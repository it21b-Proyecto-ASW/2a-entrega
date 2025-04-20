# Issue Tracker - API REST

Aplicació web per gestionar i fer seguiment d'issues (problemes, tasques i millores) en projectes de desenvolupament.

## Autors

- Richard Pie
- Marta Nuñez
- Marc Planas
- Eric Herrero

## Descripció

L'Issue Tracker és una aplicació web que permet als equips de desenvolupament gestionar i fer seguiment dels problemes, tasques i millores dels seus projectes. L'aplicació ofereix una interfície intuïtiva i moderna per crear, visualitzar, editar i eliminar issues, així com fer-ne seguiment del seu estat.

## Funcionalitats Principals

- **Gestió d'Issues**
  - Crear, editar i eliminar issues
  - Assignar tipus (bug, feature, task)
  - Definir severitat (baixa, mitjana, alta, crítica)
  - Establir estat (obert, en progrés, resolt, tancat)
  - Afegir descripcions detallades

- **Filtres i Cerca**
  - Filtrar issues per tipus, estat i severitat
  - Cercar issues per títol o descripció
  - Ordenar issues per diferents criteris

- **Interfície d'Usuari**
  - Disseny modern i responsiu
  - Targetes visuals per cada issue
  - Distintius de colors per tipus, estat i severitat
  - Navegació intuïtiva

- **Autenticació i Seguretat**
  - Inici de sessió amb Firebase
  - Gestió d'usuaris i permisos
  - Emmagatzematge segur de dades

## Tecnologies Utilitzades

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Firebase (Autenticació i Base de dades)

- **Backend**
  - API REST
  - Node.js
  - Express
  - OpenAPI/Swagger per documentació

## Estructura del Projecte

```
REST-app/
├── public/
│   ├── index.html          # Pàgina principal
│   ├── issues.html         # Gestió d'issues
│   ├── users.html          # Gestió d'usuaris
│   ├── settings.html       # Configuració
│   ├── navbar.html         # Barra de navegació
│   └── navbar.js           # Lògica de la navbar
├── server.js               # Servidor API REST
├── package.json            # Dependències
└── README.md               # Documentació
```

## Com Fer Funcionar el Projecte

### Requisits Previs

1. **Node.js i npm**
   - Instal·lar Node.js (versió 14 o superior)
   - npm s'instal·la automàticament amb Node.js
   - Verificar la instal·lació:
     ```bash
     node --version
     npm --version
     ```

2. **Firebase**
   - Crear un compte a [Firebase Console](https://console.firebase.google.com/)
   - Crear un nou projecte
   - Habilitar Authentication i Firestore Database

### Configuració del Projecte

1. **Clonar el Repositori**
   ```bash
   git clone https://github.com/it21b-Proyecto-ASW/2a-entrega.git
   cd 2a-entrega
   ```

2. **Instal·lar Dependències**
   ```bash
   npm install
   ```

3. **Configurar Firebase**
   - Anar a [Firebase Console](https://console.firebase.google.com/)
   - Seleccionar el projecte
   - Anar a "Project Settings" (⚙️)
   - A la secció "Your apps", afegir una aplicació web
   - Copiar la configuració de Firebase
   - Crear un fitxer `.env` a l'arrel del projecte:
     ```
     FIREBASE_API_KEY=la_teva_api_key
     FIREBASE_AUTH_DOMAIN=el_teu_auth_domain
     FIREBASE_PROJECT_ID=el_teu_project_id
     FIREBASE_STORAGE_BUCKET=el_teu_storage_bucket
     FIREBASE_MESSAGING_SENDER_ID=el_teu_messaging_sender_id
     FIREBASE_APP_ID=la_teva_app_id
     ```

4. **Configurar Firestore**
   - Anar a "Firestore Database" al panell de Firebase
   - Crear una base de dades en mode de producció
   - Configurar les regles de seguretat:
     ```javascript
     rules_version = '2';
     service cloud.firestore {
       match /databases/{database}/documents {
         match /{document=**} {
           allow read, write: if request.auth != null;
         }
       }
     }
     ```

### Executar l'Aplicació

1. **Iniciar el Servidor**
   ```bash
   npm run dev
   ```

2. **Accedir a l'Aplicació**
   - Obrir el navegador
   - Anar a `http://localhost:3000`
   - Registrar-se o iniciar sessió amb un compte de Firebase

3. **Provar l'API**
   - Accedir a `http://localhost:3000/api-docs` per veure la documentació de l'API
   - Provar els diferents endpoints amb Swagger UI

### Solucionar Problemes Comuns

1. **Error de Connexió amb Firebase**
   - Verificar que les credencials al `.env` són correctes
   - Comprovar que la base de dades Firestore està activada
   - Assegurar-se que les regles de seguretat permeten l'accés

2. **Problemes amb les Dependències**
   - Eliminar la carpeta `node_modules` i el fitxer `package-lock.json`
   - Executar `npm install` de nou

3. **Errors del Servidor**
   - Verificar que el port 3000 està lliure
   - Comprovar els logs del servidor per més informació

## Documentació de l'API

La documentació completa de l'API REST està disponible a `/api-docs` quan el servidor està en execució. La documentació inclou:
- Descripció de tots els endpoints
- Exemples de peticions i respostes
- Esquemes de dades
- Autenticació i autorització

## Contribucions

Les contribucions són benvingudes! Si vols contribuir al projecte:
1. Fer un fork del repositori
2. Crear una branca per a la teva funcionalitat
3. Fer commit dels canvis
4. Pujar la branca
5. Crear un Pull Request

## Llicència

Aquest projecte està sota la llicència MIT. Veure el fitxer `LICENSE` per més detalls. 