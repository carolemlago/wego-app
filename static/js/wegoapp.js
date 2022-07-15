'use strict';

// Initialize and add the map
function initMap() {

  // Locations on map
  const sanDiego = {
    title: "San Diego", 
    lat: 32.790765862212645, 
    lng: -117.1625785421353 
  };
  const losAngeles = { 
    title: "Los Angeles", 
    lat: 33.98723326876288, 
    lng: -118.24616028567611, 
  };

  const sanFrancisco = { 
    title: "San Francisco", 
    lat:  37.76730758423299, 
    lng: -122.42709150624904, 
  };
  
  const newYork = { 
    title: "New York City",
    lat:  40.75438989746753, 
    lng: -73.98795612582705, 
  };

  const portland = {
    title: "Portland", 
    lat:  45.51280391097843, 
    lng: -122.68530831643817, 
  };

  const denver = { 
    title: "Denver",
    lat:  39.746306786921615, 
    lng: -104.97391013393721, 
  };

  const miami = {
    title: "Miami", 
    lat:  25.761676154905214, 
    lng: -80.20714512965891, 
  };
  const locations = [sanDiego, losAngeles, sanFrancisco, newYork, portland, denver, miami];

  // Initial location where map is zoomed in
  const usa = {
    title: "USA",
    lat: 37.84186926742124, 
    lng: -100.53259435633592
  } 

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: usa,
  });



  // Creating markers for locations

  for (const [ i, location ] of Object.entries(locations)) {
    const marker = new google.maps.Marker({
      position: location,
      map: map,
      });


 // Event listener to location selection

    marker.addListener('click', (evt) => {
      
     
     document.querySelector('#location').selectedIndex = i;
     const zoomMap = new google.maps.Map(document.querySelector('#map'), {
      center: location,
      map: map,
      zoom: 11,
    });

    });
  };
  


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
        document.querySelector(`#plan-div${i}`).style.display ='none';
        
        alert('Your plan is deleted!');
      });

    }
  deleteButton[`${i}`].addEventListener('click', handleClickDelete);
}

//  Event handler to share event

const shareButton = document.querySelectorAll('.share');

for (let i = 0; i < shareButton.length; i++) {
    
    const handleClickShare = (evt) => {

    const planId = document.getElementById(`plan-id${i}`).value;

    const formInputs = {
      planId: planId,
      toEmail: document.getElementById(`to-email${planId}`).value,
    };

    fetch('/send_email', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.text())
      .then((responseData) => {
        
        alert('Your email was sent!');
      });

    }
  
  shareButton[`${i}`].addEventListener('click', handleClickShare);
}
}


// Create Calendar

document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  
  // AJAX request
  fetch('/get_calendar_events')
    .then(response => response.json())
    .then(responseData => {
      const today = new Date().toJSON().slice(0,10);
  
      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        initialDate: today,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        
        height: "auto",
        events: responseData
      });
    
    calendar.render();
    });
    });



  