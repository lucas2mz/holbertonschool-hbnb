function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

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
    try {
        const request = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        if (request.ok) {
            const place = await request.json();
            displayPlaceDetails(place);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '';

    const placeArticle = document.createElement('article');
    placeArticle.classList.add('place-section');

    const title = document.createElement('h3');
    title.classList.add('place-title');
    title.innerHTML = place.title;

    const host = document.createElement('p');
    host.classList.add('place-host');
    host.innerHTML = `Hosted by: ${place.owner.first_name} ${place.owner.last_name}`;

    const price = document.createElement('p');
    price.classList.add('place-price');
    price.innerHTML = `Price per night: $${place.price}`;

    const description = document.createElement('p');
    description.classList.add('place-description');
    description.innerHTML = place.description;

    const amenities = document.createElement('p');
    amenities.classList.add('place-amenities');
    amenities.innerHTML = `Amenities: ${place.amenities.join(', ')}`;

    placeArticle.appendChild(title);
    placeArticle.appendChild(host);
    placeArticle.appendChild(price);
    placeArticle.appendChild(description);
    placeArticle.appendChild(amenities);

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
            await submitReview(token, placeId, reviewText);
        });
    }
});

async function submitReview(token, placeId, reviewText) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            place_id: placeId,
            review_text: reviewText
        })
    });
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

