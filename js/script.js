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
<script>
  const isIOS = /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase());
  const isInStandaloneMode = ('standalone' in window.navigator) && window.navigator.standalone;

  if (isIOS && !isInStandaloneMode) {
    document.getElementById('ios-install-banner').style.display = 'block';
  }
</script>
