

// Login check
function checkAuthentication() {
  const token = localStorage.getItem('token');
  // const loginLink = document.getElementById('login-button');
  // const logoutLink = document.getElementsById('logout-button');

  if (token) {
    // loginLink.style.display = 'none';
    // logoutLink.style.display = 'block';
    fetchPlaces(token);
  } else {
    // loginLink.style.display = 'block'
    // logoutLink.style.display = 'none'
    window.location.href = "login.html"
  }
}

const logoutButton = document.getElementById('logout-button');
logoutButton.addEventListener('click', event => {
  localStorage.clear();
  window.location.href = 'login.html';
  alert('Successful logout');
})

document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;
  const places = document.querySelectorAll('.place-card');

  places.forEach(place => {
    const placePrice = parseFloat(place.getAttribute('data-place-price'));

    if (selectedPrice === 'All' || placePrice <= parseFloat(selectedPrice)) {
      place.style.display = 'block';
    } else {
      place.style.display = 'none';
    }
  });
});

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
    const places = await response.json();
    
    displayPlaces(places);

  }catch(error) {
    alert(`Error: ${error.message}`);
  }
}

// index
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  const srcArray = ['house1.jpg', 'house2.jpg', 'house3.jpg', 'house4.jpg', 'house5.png', 'house6.jpg', 'house7.png'];

  places.forEach((place, index) => {
    const placeArticle = document.createElement('article');
    placeArticle.classList.add('place-card');
    placeArticle.dataset.placePrice = place.price;

    placeArticle.innerHTML = `
      <h3>${place.title}</h3>
      <p class="data-price">Price per night: $${place.price}</p>
      <p>${place.description}</p>
      <p>Location: ${place.longitude}, ${place.latitude}</p>
      <div><img class="place-image" src="./images/houses/${srcArray[index]}" width="600" height="450"></div>
      <button class="details-button" data-place-id="${place.id}">View Details</button>
    `;

    placesList.appendChild(placeArticle);
  });
}

document.getElementById('places-list').addEventListener('click', event => {
    if (event.target.classList.contains('details-button')) {
      const placeId = event.target.getAttribute('data-place-id');
      window.location.href = `place.html?place_id=${placeId}`;
    }
  });

checkAuthentication();