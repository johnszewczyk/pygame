document.addEventListener('DOMContentLoaded', () => {
  fetch('item-navbar.html')
    .then(response => response.text())
    .then(html => {
      document.getElementById('nav-bar').innerHTML = html;
    })
    .catch(error => {
      console.error('Error loading navbar:', error);
    });
});