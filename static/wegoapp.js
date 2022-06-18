'use strict';

// Initialize and add the map
function initMap() {
  const sanDiego = { 
    lat: 32.790765862212645, 
    lng: -117.1625785421353 
  }; 
  
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: sanDiego,
  });

  const marker = new google.maps.Marker({
    position: sanDiego,
    map: map,
  });




  
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userAddress }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;

        // Create a marker
        new google.maps.Marker({
          position: userLocation,
          map,
        });

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(18);
      } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
    });
  }

const yes_button = document.getElementByName('yes');


const handleClickYes = (evt) => {
	evt.preventDefault();
	alert('Your date is confirmed!');
};

button.addEventListener('click', handleClickYes);

const no_button = document.getElementByName('no');

const handleClickNo = (evt) => {
	evt.preventDefault();
	alert('Event deleted!');
};

button.addEventListener('click', handleClickNo);

// fetch('/save_plan', {
// 	method : 'POST',
// 	body : JSON.stringify(),
//   headers: {
//     'Content Type' : 'application/json'
//   },
// })
//   .then((response) => response.json())
//   .then((responseData) => {
//     document.getElementByName('').value = responseData;
//   });

