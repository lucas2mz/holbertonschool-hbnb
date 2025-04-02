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

// Login check
function checkAuthentication() {
  const token = localStorage.getItem('token');

  if (token) {
    fetchPlaces(token);
  } else {
    window.location.href = "/login.html"
  }
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

  places.forEach(place => {
    const placeArticle = document.createElement('article');
    placeArticle.classList.add('place-card');
    placeArticle.setAttribute('data-place-price', place.price);

    const title = document.createElement('h3');
    title.innerHTML = place.title;

    const price = document.createElement('p');
    price.classList.add('data-price');
    price.innerHTML = `Price per night: $${place.price}`;

    const description = document.createElement('p');
    description.innerHTML = place.description;

    const location = document.createElement('p');
    location.innerHTML = `Location: ${place.longitude}, ${place.latitude}`; // Cambiar a x,y

    const div = document.createElement('div');

    const image = document.createElement('img');
    image.classList.add('place-image');
    const src = srcArray[places.indexOf(place)];
    image.src = `./images/houses/${src}`;
    image.width = 600;
    image.height = 450;

    div.appendChild(image);

    const button = document.createElement('button');
    button.setAttribute('data-place-id', place.id);
    button.innerHTML = 'View Details';
    button.classList.add('details-button');

    placeArticle.appendChild(title);
    placeArticle.appendChild(price);
    placeArticle.appendChild(description);
    placeArticle.appendChild(location);
    placeArticle.appendChild(div);
    placeArticle.appendChild(button);

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