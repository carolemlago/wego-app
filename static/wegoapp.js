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
    geocoder.geocode({ address: "sanDiego" }, (results, status) => {
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





//  Event handler to delete event

const deleteButton = document.querySelectorAll('.delete');

for (let i = 0; i < deleteButton.length; i++) {
    const handleClickDelete = (evt) => {
    // Delete event from dashboard
      
    const formInputs = {
      planId: document.getElementById(`plan-id${i}`).value,
    };
    
    fetch('/delete_plan', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.text())
      .then((responseData) => {
        document.querySelector(`#plan-div${i}`).remove();
        
        alert('Your plan is deleted!');
      });

    }
  deleteButton[`${i}`].addEventListener('click', handleClickDelete);
}



