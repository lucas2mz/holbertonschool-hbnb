function checkAuthentication() {
    const token = localStorage.getItem('token');
    const loginLink = document.getElementById('login-link');

    if (token) {
        fetchPlaces(token);
    } else {
        window.location.href = 'login.html';
    }
}

async function fetchPlaces(token) {
    try{
        const request = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (request.ok) {
            const places = await request.json();
            displayPlaces(places);
        } else {
            console.error('Error fetching places:', request.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';


    places.forEach(place => {
        const placeArticle = document.createElement('article');
        placeArticle.classList.add('place-card');
        placeArticle.setAttribute('data-place-price', place.price);

        const title = document.createElement('h3');
        title.innerHTML = place.title;

        const description = document.createElement('p');
        description.innerHTML = place.description;

        const price = document.createElement('p');
        price.innerHTML = `Price per night: $${place.price}`;

        const location = document.createElement('p');
        location.innerHTML = `Location: ${place.longitude}, ${place.latitude}`;

        const button = document.createElement('button');
        button.setAttribute('data-place-id', place.id);
        button.innerHTML = 'View Details';
        button.classList.add('details-button');
    
    });
        placeArticle.appendChild(title);
        placeArticle.appendChild(description);
        placeArticle.appendChild(price);
        placeArticle.appendChild(location);
        placeArticle.appendChild(button);

        placesList.appendChild(placeArticle);
    }

checkAuthentication();