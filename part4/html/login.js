/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Your code to handle form submission
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
              await loginUser(email, password);
            } catch (error) {
              console.error('Error:', error);
              alert('Error to Login');
            }
          });
        }
});

async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    // Handle the response
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      alert('Login successful');
      window.location.href = 'index.html';
  } else {
      alert('Login failed: ' + response.statusText);
  }
} catch (error) {
  console.error('Error request:', error)
  alert('Could not connect to the server')
}
}