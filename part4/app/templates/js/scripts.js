document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;
  const places = document.querySelectorAll('.place');

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

  places.forEach(place => {
    const placeArticle = document.createElement('article');
    placeArticle.classList.add('place-card');
    placeArticle.setAttribute('data-place-price', place.price);

    const title = document.createElement('h3');
    title.innerHTML = place.title;

    const price = document.createElement('p');
    price.classList.add('data-price');
    price.innerHTML = place.price;

    const description = document.createElement('p');
    description.innerHTML = place.description;

    const location = document.createElement('p');
    location.innerHTML = `Location: ${place.location}`; // Cambiar a x,y

    const button = document.createElement('button');
    button.innerHTML = 'View Details';
    button.classList.add('details-button');

    placeArticle.appendChild(title);
    placeArticle.appendChild(description);
    placeArticle.appendChild(location);
    placeArticle.appendChild(button);

    placesList.appendChild(placeArticle);
  });
}

checkAuthentication()

// function getPlaceIdFromURL() {
//   const params = new URLSearchParams(window.location.search);
//   return params.get('place_id');
// }

// // Place check
// function checkAuthentication() {
//   const token = getCookie('token');
//   const addReviewSection = document.getElementById('add-review');

//   if (!token) {
//       addReviewSection.style.display = 'none';
//   } else {
//       addReviewSection.style.display = 'block';
//       // Store the token for later use
//       const placeId = getPlaceIdFromURL();
//       fetchPlaceDetails(token, placeId);
//   }
// }

// async function fetchPlaceDetails(token, placeId) {
//   // Make a GET request to fetch place details
//   try {
//     const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         'Authorization': `Bearer ${token}`
//       }
//     });
//     if (!response.ok) {
//       throw new Error('Failed to fetch place details');
//     }

//     const place = await response.json();

//     displayPlaceDetails(place);
  
//   }catch(error) {
//     alert(`Error: ${error.message}`);
//   }
// }

// function displayPlaceDetails(place) {
//   const placeDetails = document.getElementById('place-details');
//   placeDetails.innerHTML = '';

//   place.array.forEach(place => {
//     const placeDiv = document.createElement('div');
//     placeDiv.classList.add('place-section');

//     const placeDiv2 = document.createElement('div');
//     placeDiv2.classList.add('text-content');

//     const title = document.createElement('h2');
//     title.classList.add('place-info-title');
//     title.innerHTML = place.title;

//     const host = document.createElement('p');
//     host.classList.add('place-info');
//     host.innerHTML = `Host: ${place.host}`;

//     const price = document.createElement('p');
//     price.classList.add('place-info');
//     price.innerHTML = `Price per night: ${place.price}`;

//     const description = document.createElement('p');
//     description.classList.add('place-info');
//     description.innerHTML = `Description: ${place.description}`;

//     const amenities = document.createElement('p');
//     amenities.classList.add('place-info');
//     amenities.innerHTML = `Amenities: ${place.amenities}`;

//     if (place.reviews) {
//       const reviews = document.createElement('p');
//       reviews.classList.add('place-info');
//       reviews.innerHTML = `Reviews: ${place.reviews}`;
//       placeArticle.appendChild(reviews);
//     }

//     placeDiv2.appendChild(title);
//     placeDiv2.appendChild(host);
//     placeDiv2.appendChild(price);
//     placeDiv2.appendChild(description);
//     placeDiv2.appendChild(amenities);

//     placeDetails.appendChild(placeDiv);
//     placeDetails.appendChild(placeDiv2);
//   });
// }

// // Check for adding a review
// function checkAuthentication() {
//   const token = getCookie('token');
//   if (!token) {
//       window.location.href = 'index.html';
//   }
//   return token;
// }

// document.addEventListener('DOMContentLoaded', () => {
//   const reviewForm = document.getElementById('review-form');
//   const token = checkAuthentication();
//   const placeId = getPlaceIdFromURL();

//   if (reviewForm) {
//       reviewForm.addEventListener('submit', async (event) => {
//           event.preventDefault();
//           const formData = new FormData(reviewForm);
//           // Get review text from form
//           const reviewText = formData.get('text');
//           await submitReview(token, placeId, reviewText);
//       });
//   }
// });
// // SUBMIT REVIEW (no se si esta bien)
// async function submitReview(token, placeId, reviewText, userId, rating) {
//   const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'Authorization': `Bearer ${token}`
//     },
//     body: JSON.stringify({ placeId, reviewText, userId, rating })
//   });
//   handleResponse(response);
// }

// function handleResponse(response) {
//   if (response.ok) {
//       alert('Review submitted successfully!');
//       // Clear the form
//   } else {
//       alert('Failed to submit review');
//   }
// }