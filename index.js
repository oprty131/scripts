const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// Middleware to handle form data
app.use(express.urlencoded({ extended: true }));

// Serve static files (HTML page)
app.use(express.static(path.join(__dirname, 'public')));

// Handle script upload via POST request
app.post('/upload', (req, res) => {
    const scriptName = req.body.scriptName.trim();
    const scriptContent = req.body.scriptContent;

    // Sanitize the script name to avoid illegal file names
    const sanitizedScriptName = scriptName.replace(/[^a-zA-Z0-9-_]/g, '') + '.lua';

    // Save the script content to a .lua file in the uploads folder
    const scriptPath = path.join(__dirname, 'uploads', sanitizedScriptName);
    fs.writeFile(scriptPath, scriptContent, (err) => {
        if (err) {
            console.error('Error saving script:', err);
            return res.status(500).send('Error uploading the script.');
        }
        res.send('Script uploaded successfully! <a href="/">Go back</a>');
    });
});

// Serve raw Lua scripts from the 'uploads' folder
app.get('/raw/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.params.filename);
    res.sendFile(filePath);
});

// Endpoint to get the list of available scripts
app.get('/scripts', (req, res) => {
    fs.readdir(path.join(__dirname, 'uploads'), (err, files) => {
        if (err) {
            console.error('Error reading directory:', err);
            return res.status(500).send('Error loading scripts.');
        }
        // Only return .lua files
        const luaFiles = files.filter(file => file.endsWith('.lua'));
        res.json(luaFiles);
    });
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
