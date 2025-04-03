function checkAuthentication() {
    const token = localStorage.getItem('token');
  
    if (token) {
      fetchPlaces(token);
    } else {
      window.location.href = "login.html"
    }
  }

const logoutButton = document.getElementById('logOut-button');
logoutButton.addEventListener('click', event => {
localStorage.clear();
window.location.href = 'login.html';
alert('Successful logout');
})

async function fetchPlaces(token) {
    console.log(token);
    try{
        const request = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (request.ok) {
            const places = await request.json();
            console.log(places);
            displayPlaces(places);
        } else {
            console.error('Error fetching places:', request.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaces(places) {
    console.log(places);
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    const imageArray = ["casa_1_sala.png", "casa_2_sala.png", "casa_3_sala.png"];

    places.forEach((place, index) => {
        const placeArticle = document.createElement('article');
        placeArticle.classList.add('place-card');
        placeArticle.setAttribute('data-place-price', place.price);

        const title = document.createElement('h3');
        title.innerHTML = place.title;

        const description = document.createElement('p');
        description.innerHTML = place.description;

        const price = document.createElement('p');
        price.classList.add('data-price');
        price.innerHTML = `Price per night: $${place.price}`;

        const location = document.createElement('p');
        location.innerHTML = `Location: ${place.longitude}, ${place.latitude}`;

        placeDiv = document.createElement('div');
        placeDiv.innerHTML = `<img class="place-image" src="./images/${imageArray[index]}" width="300" height="150">`;

        const button = document.createElement('button');
        button.setAttribute('data-place-id', place.id);
        button.innerHTML = 'View Details';
        button.classList.add('details-button');
    

        placeArticle.appendChild(title);
        placeArticle.appendChild(description);
        placeArticle.appendChild(price);
        placeArticle.appendChild(location);
        placeArticle.appendChild(button);
        placeArticle.appendChild(placeDiv);

        placesList.appendChild(placeArticle);
    });
    }

checkAuthentication();