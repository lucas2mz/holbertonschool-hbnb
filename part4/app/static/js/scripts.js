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
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      }catch (err) {
        console.error('Error parsing response:', err);
      }
      throw new Error(errorMessage);
    }

    /* data del usuario, si el login se realiza correctamente */
    const data = await response.json()

    /* almacena el token JWT y asigna las cookies */
    if (data.access_token) {
      document.cookie = `token=${data.access_token}; path=/`;
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
    placeArticle.classList.add('place-card');

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

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
      addReviewSection.style.display = 'none';
  } else {
      addReviewSection.style.display = 'block';
      // Store the token for later use
      const placeId = getPlaceIdFromURL();
      fetchPlaceDetails(token, placeId);
  }
}

async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const place = await response.json();

    return place;
  
  }catch(error) {
    alert(`Error: ${error.message}`);
  }
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');
  placeDetails.innerHTML = '';

  place.array.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.classList.add('place-section');

    const placeDiv2 = document.createElement('div');
    placeDiv2.classList.add('text-content');

    const title = document.createElement('h2');
    title.classList.add('place-info-title');
    title.innerHTML = place.title;

    const host = document.createElement('p');
    host.classList.add('place-info');
    host.innerHTML = `Host: ${place.host}`;

    const price = document.createElement('p');
    price.classList.add('place-info');
    price.innerHTML = `Price per night: ${place.price}`;

    const description = document.createElement('p');
    description.classList.add('place-info');
    description.innerHTML = `Description: ${place.description}`;

    const amenities = document.createElement('p');
    amenities.classList.add('place-info');
    amenities.innerHTML = `Amenities: ${place.amenities}`;

    if (place.reviews){
      const reviews = document.createElement('p');
      reviews.classList.add('place-info');
      reviews.innerHTML = `Reviews: ${place.reviews}`;
      placeArticle.appendChild(reviews);
    }

    placeDiv2.appendChild(title);
    placeDiv2.appendChild(host);
    placeDiv2.appendChild(price);
    placeDiv2.appendChild(description);
    placeDiv2.appendChild(amenities);

    placeDetails.appendChild(placeDiv);
    placeDetails.appendChild(placeDiv2);
  });
}