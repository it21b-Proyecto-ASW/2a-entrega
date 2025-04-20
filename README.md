# Issue Tracker App

Aplicació web per gestionar issues amb autenticació d'usuaris i funcionalitats de comentaris.

## Característiques

- Autenticació amb Google i email/password
- Gestió d'issues amb camps personalitzats
- Sistema de comentaris per issue
- Ordenació d'issues per prioritat
- Gestió de perfils d'usuari amb imatges de perfil
- Pujada d'arxius adjunts

## Tecnologies

- Firebase (Authentication, Firestore, Storage)
- Express.js
- JavaScript
- HTML/CSS

## Estructura del Projecte

```
src/
  ├── config/        # Configuració de Firebase i altres
  ├── controllers/   # Controladors de l'aplicació
  ├── middleware/    # Middleware personalitzat
  ├── models/        # Models de dades
  ├── routes/        # Rutes de l'API
  └── public/        # Arxius estàtics
```

## Instal·lació

1. Clonar el repositori
2. Executar `npm install`
3. Configurar les variables d'entorn al fitxer `.env`
4. Executar `npm start` 