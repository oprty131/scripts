const scripts = [];

// Function to upload script
function uploadScript() {
    const name = document.getElementById('scriptName').value;
    const content = document.getElementById('scriptContent').value;

    if (name && content) {
        // Create a Blob from the script content
        const blob = new Blob([content], { type: 'text/plain' });
        const scriptUrl = URL.createObjectURL(blob); // Create a URL for the Blob
        scripts.push({ name, url: scriptUrl }); // Add to the scripts array

        // Reset input fields
        document.getElementById('scriptName').value = '';
        document.getElementById('scriptContent').value = '';

        // Update the script list
        updateScriptList();
    } else {
        alert('Please enter both the script name and content.');
    }
}

// Function to update the script list display
function updateScriptList() {
    const scriptList = document.getElementById('scriptList');
    scriptList.innerHTML = ''; // Clear the current list
    scripts.forEach(script => {
        const listItem = document.createElement('li');
        // Create a link to the Blob URL for each script
        listItem.innerHTML = `<a href="${script.url}" target="_blank">${script.name} (Raw)</a>`;
        scriptList.appendChild(listItem);
    });
}
