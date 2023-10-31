const express = require('express');
const multer = require('multer');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Configura multer para guardar archivos en la carpeta de uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Directorio donde se guardarán los videos (basado en el ID del usuario)
    const id_user = req.body.full_name; // Asegúrate de que este campo sea el ID del usuario
    cb(null, `uploads/${id_user}`);
  },
  filename: (req, file, cb) => {
    // Define el nombre del archivo (puedes personalizarlo)
    cb(null, `video_${Date.now()}.webm`);
  },
});

const upload = multer({ storage });

app.use(bodyParser.json());

// Ruta para subir un video
app.post('/Vídeos', upload.single('video'), (req, res) => {
  res.status(200).send('Video guardado con éxito.');
});

app.listen(port, () => {
  console.log(`Servidor en ejecución en el puerto ${port}`);
});
