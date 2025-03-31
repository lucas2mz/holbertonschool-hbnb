const loginForm = document.getElementById('login-form');

if (loginForm) {
  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(loginForm);
    const email = formData.get('email');
    const password = formData.get('password');

    await loginUser(email, password);
  });
}

async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok){
      let errorMessage = 'Login failed';
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      }catch (err) {
        console.error('Error parsing response:', err);
      }
      throw new Error(errorMessage);
    }

    /* data del usuario, si el login se realiza correctamente */
    const data = await response.json();

    /* asigna las cookies */
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      alert('Login successful');
      window.location.href = 'index.html';
    }
    else{
      throw new Error('No token received');
    }
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}

