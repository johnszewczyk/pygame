
// report that this file was loaded to the website
// document.addEventListener('DOMContentLoaded', (event) => {
//   document.getElementById('client-type-d').textContent = "🖥️";
// });

// alt. input handler that returns focus to terminal for keyboard users
function handleInput(buttonMap, key) {
  sendInput(key);
  buttonMap[key].classList.add('active');
  setTimeout(function () {
    buttonMap[key].classList.remove('active');
  }, 100); // Reset visual feedback (adjust timing as needed)
}

