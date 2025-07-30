console.log("script.js loaded!");

document.addEventListener('DOMContentLoaded', () => {
    const moduleButtons = document.querySelectorAll('.module-button');

    moduleButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const moduleId = event.currentTarget.id;
            // Navigate to the corresponding HTML page for the module
            window.location.href = moduleId + '.html'; 
        });
    });
});
