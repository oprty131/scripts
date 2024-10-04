// Function to upload script
function uploadScript() {
    const name = document.getElementById('scriptName').value;
    const content = document.getElementById('scriptContent').value;

    if (name && content) {
        // Store the script content in localStorage
        localStorage.setItem(name, content);

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
    for (let i = 0; i < localStorage.length; i++) {
        const name = localStorage.key(i);
        const content = localStorage.getItem(name);
        // Create a raw link using a data URL
        const rawLink = `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`;
        const listItem = document.createElement('li');
        listItem.innerHTML = `<a href="${rawLink}" target="_blank">${name} (Raw)</a>`;
        scriptList.appendChild(listItem);
    }
}

// Load scripts from localStorage on page load
window.onload = function () {
    updateScriptList(); // Initialize the script list
};
