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

  let reviewsHTML = '<h3 class="place-review">Reviews</h3><br>';

  if (place.reviews && place.reviews.length > 0){
    reviewsHTML += '<dl class="review-card">';
    place.reviews.forEach(review => {
      reviewsHTML += `
          <dt>${review.first_name} ${review.last_name}</dt>
          <dd>${review.rating = "★".repeat(review.rating)}</dd>
          <dd>${review.text}</dd>
      `;
    });
    reviewsHTML += '</dl>'
  }else {
    reviewsHTML = '<h1><strong>This Place dont have any reviews yet.</strong></h1><br>'
  }

  const placeDiv = document.createElement('div');
  placeDiv.classList.add('text-content');

  placeDiv.innerHTML = `
    <h2 class="place-info-title">${place.title}</h2>
    <p class="place-info">Host: ${place.owner.first_name} ${place.owner.last_name}</p>
    <p class="place-info">Price per night: $${place.price}</p>
    <p class="place-info">Description: ${place.description}</p>
  `;

  const reviews = document.createElement('p');
  reviews.innerHTML = `
    ${reviewsHTML}
  `;

  const placeDiv2 = document.createElement('div');
  placeDiv2.classList.add('place-image');
  placeDiv2.innerHTML = `<img src="./images/houses/house5.png" width="600" height="450">`;

  placeDiv.appendChild(placeDiv2);
  placeDiv.appendChild(reviews)
  placeArticle.appendChild(placeDiv);
  placeDetails.appendChild(placeArticle);
}

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const formData = new FormData(reviewForm);
          const reviewText = formData.get('review-text');
          const rating = formData.get('rating');
          await submitReview(token, placeId, reviewText, rating);
      });
  }
});
// SUBMIT REVIEW 
async function submitReview(token, placeId, reviewText, rating) {
  rating = parseInt(rating, 10);
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
  } else {
      alert('Failed to submit review');
  }
}

checkAuthentication();
