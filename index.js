const express = require('express');
const path = require('path');
const multer = require('multer');
const app = express();

// Set storage engine for Multer (file upload handler)
const storage = multer.diskStorage({
    destination: './uploads/',
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});

// Initialize Upload
const upload = multer({ storage: storage }).single('scriptFile');

// Serve static files (HTML page)
app.use(express.static(path.join(__dirname, 'public')));

// Handle file upload through POST request
app.post('/upload', (req, res) => {
    upload(req, res, (err) => {
        if (err) {
            res.send('Error uploading the file.');
        } else {
            res.send('File uploaded successfully! <a href="/">Go back</a>');
        }
    });
});

// Serve raw Lua scripts from 'uploads' folder
app.get('/raw/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.params.filename);
    res.sendFile(filePath);
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
