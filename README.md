#segona entrega del projecte de ASW
Autors:
  - Richard Pie
  - Marta Nuñez
  - Marc Planas
  - Eric Herrero

# Issue Tracker

Aplicació web per gestionar issues desenvolupada amb Django.

## Requisits

- Python 3.8 o superior
- pip (gestor de paquets de Python)
- Git (opcional, per clonar el repositori)

## Instal·lació ràpida

### Windows
1. Executa el script `update.ps1`:
```powershell
.\update.ps1
```

### Linux
1. Fes el script executable:
```bash
chmod +x update.sh
```
2. Executa'l:
```bash
./update.sh
```

El script farà automàticament:
- Crear i activar l'entorn virtual
- Instal·lar totes les dependències
- Aplicar les migracions
- Iniciar el servidor de desenvolupament

## Instal·lació manual

Si prefereixes fer els passos manualment:

### Windows

1. Obre PowerShell o CMD i navega fins al directori del projecte:
```powershell
cd ruta/al/directori/del/projecte
```

2. Crea un entorn virtual:
```powershell
python -m venv .venv
```

3. Activa l'entorn virtual:
```powershell
.\.venv\Scripts\activate
```

4. Instal·la les dependències:
```powershell
pip install -r requirements.txt
```

5. Aplica les migracions:
```powershell
python manage.py migrate
```

6. Inicia el servidor de desenvolupament:
```powershell
python manage.py runserver
```

### Linux

1. Obre el terminal i navega fins al directori del projecte:
```bash
cd ruta/al/directori/del/projecte
```

2. Crea un entorn virtual:
```bash
python3 -m venv .venv
```

3. Activa l'entorn virtual:
```bash
source .venv/bin/activate
```

4. Instal·la les dependències:
```bash
pip install -r requirements.txt
```

5. Aplica les migracions:
```bash
python manage.py migrate
```

6. Inicia el servidor de desenvolupament:
```bash
python manage.py runserver
```

## Accés a l'aplicació

Un cop el servidor estigui funcionant, pots accedir a l'aplicació a través del navegador:
```
http://127.0.0.1:8000/
```

## URLs principals

- `/issues` - Llista d'issues
- `/new` - Crear nova issue
- `/edit` - Editar issue
- `/users` - Llista d'usuaris
- `/settings` - Configuració

## Notes

- Assegura't que tens totes les variables d'entorn necessàries configurades al fitxer `.env`
- El servidor de desenvolupament no és adequat per entorns de producció
- Per aturar el servidor, prem `Ctrl+C` al terminal

## Features

- User authentication with Google OAuth
- Issue creation, editing, and deletion
- File attachments for issues
- Comments on issues
- Issue filtering and search
- User management
- Configuration management for issue types, states, priorities, and severities

## Configuració

1. Instal·la les dependències:
```bash
pip install -r requirements.txt
```

2. Configura les variables d'entorn:
- Crea un fitxer `.env` a l'arrel del projecte
- Afegeix les següents variables amb els teus valors de Firebase:
```
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
```

3. Executa les migracions:
```bash
python manage.py migrate
```

4. Inicia el servidor:
```bash
python manage.py runserver
```

## API REST Endpoints

### Autenticació
- `POST /api-token-auth/`: Obtenir token d'autenticació

### Issues
- `GET /api/issues/`: Llistar tots els issues
- `POST /api/issues/`: Crear un nou issue
- `GET /api/issues/{id}/`: Obtenir detalls d'un issue
- `PUT /api/issues/{id}/`: Actualitzar un issue
- `DELETE /api/issues/{id}/`: Eliminar un issue
- `POST /api/issues/{id}/add_comment/`: Afegir un comentari
- `POST /api/issues/{id}/upload_attachment/`: Pujar un arxiu
- `POST /api/issues/{id}/add_watcher/`: Afegir un observador
- `POST /api/issues/{id}/remove_watcher/`: Eliminar un observador

### Comentaris
- `GET /api/comments/`: Llistar tots els comentaris
- `POST /api/comments/`: Crear un nou comentari
- `GET /api/comments/{id}/`: Obtenir detalls d'un comentari
- `PUT /api/comments/{id}/`: Actualitzar un comentari
- `DELETE /api/comments/{id}/`: Eliminar un comentari

### Arxius
- `GET /api/attachments/`: Llistar tots els arxius
- `POST /api/attachments/`: Pujar un nou arxiu
- `GET /api/attachments/{id}/`: Obtenir detalls d'un arxiu
- `DELETE /api/attachments/{id}/`: Eliminar un arxiu

### Usuaris
- `GET /api/users/`: Llistar tots els usuaris
- `GET /api/users/{id}/`: Obtenir detalls d'un usuari

### Configuració
- `GET /api/tipos/`: Llistar tipus d'issues
- `GET /api/estados/`: Llistar estats d'issues
- `GET /api/prioridades/`: Llistar prioritats d'issues
- `GET /api/severidades/`: Llistar severitats d'issues

## Autenticació

Per utilitzar l'API, necessites obtenir un token d'autenticació:

```bash
curl -X POST http://localhost:8000/api-token-auth/ -d "username=user&password=pass"
```

Després, inclou el token en les capçaleres de les peticions:

```bash
curl -H "Authorization: Token your_token" http://localhost:8000/api/issues/
```

# ASW Project - 2a Entrega

## Descripció
Aquest projecte és una aplicació web desenvolupada amb Django que permet gestionar usuaris, perfils i publicacions.

## Requisits
- Python 3.8 o superior
- pip (gestor de paquets de Python)
- PostgreSQL
- Node.js i npm (per al frontend)

## Instal·lació

### 1. Configuració de l'entorn virtual
```bash
# Crear l'entorn virtual
python -m venv venv

# Activar l'entorn virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Instal·lar dependències
```bash
pip install -r requirements.txt
```

### 3. Configuració de la base de dades
```bash
# Crear la base de dades PostgreSQL
createdb asw_db

# Fer les migracions
python manage.py makemigrations
python manage.py migrate
```

### 4. Configuració de les variables d'entorn
Crea un arxiu `.env` a la carpeta arrel del projecte amb les següents variables:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/asw_db
```

### 5. Executar el servidor
```bash
# Windows:
.\update.bat
# o
.\update.ps1

# Linux/Mac:
./update.ps1
```

## Estructura del projecte
- `users/`: Aplicació per a la gestió d'usuaris i perfils
- `posts/`: Aplicació per a la gestió de publicacions
- `templates/`: Plantilles HTML
- `static/`: Arxius estàtics (CSS, JS, imatges)
- `media/`: Arxius pujats pels usuaris

## Funcionalitats principals
- Registre i autenticació d'usuaris
- Gestió de perfils d'usuari
- Publicació i gestió de contingut
- Sistema de seguidors
- Comentaris en publicacions

## Contribució
1. Fer fork del projecte
2. Crear una branca per a la teva feature (`git checkout -b feature/AmazingFeature`)
3. Commit dels canvis (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branca (`git push origin feature/AmazingFeature`)
5. Obrir un Pull Request

## Llicència
Aquest projecte està sota la llicència MIT. Veure el fitxer `LICENSE` per a més detalls.
