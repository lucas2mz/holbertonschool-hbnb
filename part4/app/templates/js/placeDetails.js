function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
}

// Place check
function checkAuthentication() {
  const token = localStorage.getItem('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
      addReviewSection.style.display = 'none';
  } else {
      addReviewSection.style.display = 'block';
      const placeId = getPlaceIdFromURL();
      fetchPlaceDetails(token, placeId);
  }
  return token
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

    displayPlaceDetails(place);
  
  }catch(error) {
    alert(`Error: ${error.message}`);
  }
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');
  placeDetails.innerHTML = '';

  const placeArticle = document.createElement('article');
  placeArticle.classList.add('place-section');

  const placeDiv = document.createElement('div');
  placeDiv.classList.add('text-content');

  const title = document.createElement('h2');
  title.classList.add('place-info-title');
  title.innerHTML = place.title;

  const host = document.createElement('p');
  host.classList.add('place-info');
  host.innerHTML = `Host: ${place.owner.first_name}`;

  const price = document.createElement('p');
  price.classList.add('place-info');
  price.innerHTML = `Price per night: ${place.price}`;

  const description = document.createElement('p');
  description.classList.add('place-info');
  description.innerHTML = `Description: ${place.description}`;

  const amenities = document.createElement('p');
  amenities.classList.add('place-info');
  amenities.innerHTML = `Amenities: ${place.amenities}`;

  const image = document.createElement('img');
  image.classList.add('place-image');
  image.src = `./images/houses/house5.png`;
  image.width = 600;
  image.height = 450;

  placeDiv.appendChild(title);
  placeDiv.appendChild(host);
  placeDiv.appendChild(price);
  placeDiv.appendChild(description);
  placeDiv.appendChild(amenities);
  placeDiv.appendChild(image);

  placeDetails.appendChild(placeArticle);
  placeDetails.appendChild(placeDiv);
}

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const formData = new FormData(reviewForm);
          const reviewText = formData.get('text');
          const rating = formData.get('rating');
          await submitReview(token, placeId, reviewText, rating);
      });
  }
});
// SUBMIT REVIEW (corregir)
async function submitReview(token, placeId, reviewText, rating) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ place_id: placeId, text: reviewText, rating })
  });
  handleResponse(response);
}

function handleResponse(response) {
  if (response.ok) {
      alert('Review submitted successfully!');
      // Clear the form
  } else {
      alert('Failed to submit review');
  }
}

checkAuthentication();
