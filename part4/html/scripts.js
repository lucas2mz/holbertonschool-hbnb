document.addEventListener('DOMContentLoaded', () => {
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
});

document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;
  const places = document.querySelectorAll('.place');

  places.forEach(place => {
    const placePrice = parseFloat(place.getAttribute('data-price'));

    if (selectedPrice === 'All' || placePrice <= parseFloat(selectedPrice)) {
      place.style.display = 'block';
    } else {
      place.style.display = 'none';
    }
  });
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

    if (!response.ok){
      let errorMessage = 'Login failed'
      try {
        const erroData = await response.json();
        errorMessage = erroData.message || errorMessage;
      }catch (err) {

      }
      throw new Error(errorMessage);
    }

    /* data del usuario, si el login se realiza correctamente */
    const data = await response.json()

    /* almacena el token JWT y asigna las cookies */
    if (data.token) {
      localStorage.setItem('authToken', data.token);
      document.cookie = `token=${data.access_token}; path=/`;
    }
    alert('Login successful');
    window.location.href = 'index.html';
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
  }
}
function getCookie(name) {
  // Function to get a cookie value by its name
  const cookies = document.cookie.split("; ");
  for (let cookie in cookies) {
    const [key, value] = cookie.split("=");
    if (key == name) {
      return decodeURIComponent(value);
    }
  }
  return null;
}

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    const data = await response.json();
  
  }catch(error) {
    alert(`Error: ${error.message}`);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('place-list');
  placesList.innerHTML = '';

  places.array.forEach(place => {
    const placeArticle = document.createElement('article');
    placeArticle.classList.add('place');

    const name = document.createElement('h3');
    name.innerHTML = place.name;

    const description = document.createElement('p');
    description.innerHTML = place.description;

    const location = document.createElement('p');
    location.innerHTML = `Location: ${place.location}`;

    placeArticle.appendChild(name);
    placeArticle.appendChild(description);
    placeArticle.appendChild(location);

    placesList.appendChild(placeArticle);
  });
}