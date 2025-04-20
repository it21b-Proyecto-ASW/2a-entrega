# Issue Tracker - API REST

Aplicació web per gestionar i fer seguiment d'issues (problemes, tasques i millores) en projectes de desenvolupament.

## Autors

- Richard Pie
- Marta Nuñez
- Marc Planas
- Eric Herrero


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

### Configuració del Projecte

1. **Clonar el Repositori**
   ```bash
   git clone https://github.com/it21b-Proyecto-ASW/2a-entrega.git
   cd 2a-entrega
   ```

2. **Instal·lar Dependències**
   ```bash
   npm install express cors multer firebase-admin dotenv
   ```

3. **Configurar el Servidor**
   - Assegurar-se que el port 3000 està lliure
   - Si el port 3000 està en ús, canviar el port al fitxer `server.js`

### Executar l'Aplicació

1. **Iniciar el Servidor**
   ```bash
   node server.js
   ```

2. **Accedir a l'Aplicació**
   - Obrir el navegador
   - Anar a `http://localhost:3000`
   - Registrar-se o iniciar sessió amb un compte de Firebase

### Solucionar Problemes Comuns

1. **Problemes amb les Dependències**
   - Eliminar la carpeta `node_modules` i el fitxer `package-lock.json`
   - Executar `npm install` de nou

2. **Errors del Servidor**
   - Verificar que el port 3000 està lliure
   - Comprovar els logs del servidor per més informació

