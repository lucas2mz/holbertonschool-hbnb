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

  place.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.classList.add('place-section');

    const placeDiv2 = document.createElement('div');
    placeDiv2.classList.add('text-content');

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

    if (place.reviews) {
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

checkAuthentication();

// Check for adding a review
function checkAuthentication() {
  const token = localStorage.getItem('token');

  if (token) {
    return token;
  } else{
    window.location.href = 'index.html';
  }
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
async function submitReview(token, placeId, reviewText, userId, rating) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ placeId, reviewText, userId, rating })
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