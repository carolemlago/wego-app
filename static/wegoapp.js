const travel_options = {
	method: 'GET',
	headers: {
		'X-RapidAPI-Key': 'b3729dfa39mshd1e8aaba11e2d09p172207jsn6f061d1e32af',
		'X-RapidAPI-Host': 'booking-com.p.rapidapi.com'
	}
};

fetch('https://booking-com.p.rapidapi.com/v1/metadata/exchange-rates?currency=USD&locale=en-us', travel_options)
	.then(response => response.json())
	.then(response => console.log(response))
	.catch(err => console.error(err));


const weekend_options = {
    method: 'GET',
    headers: {
        // 'API-Key': 'ptlUyUapPefNWzQN_teSPT63SL9KGJI6xWXg8rpw3HJ8QCPJm93D6WYgtH0Upw0HGKisK5xuMngtELHafA-2_dJnCp5-kJtnUujNG5WQRTgywKSG-FcQChQE3ACoYnYx',
        // 'Yelp Fusion API': 'https://api.yelp.com/v3/events/featured'
       }
    };
                
    fetch('https://api.yelp.com/v3/events/featured', weekend_options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));


const date_options = {
    method: 'GET',
    headers: {
        // 'API-Key': 'ptlUyUapPefNWzQN_teSPT63SL9KGJI6xWXg8rpw3HJ8QCPJm93D6WYgtH0Upw0HGKisK5xuMngtELHafA-2_dJnCp5-kJtnUujNG5WQRTgywKSG-FcQChQE3ACoYnYx',
        // 'Yelp Fusion API': 'https://api.yelp.com/v3/events/featured'
        }
    };
    
    fetch('https://api.yelp.com/v3/events/featured', date_options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));
    
    


// const yelp = require('yelp-fusion');
// const client = yelp.client('ptlUyUapPefNWzQN_teSPT63SL9KGJI6xWXg8rpw3HJ8QCPJm93D6WYgtH0Upw0HGKisK5xuMngtELHafA-2_dJnCp5-kJtnUujNG5WQRTgywKSG-FcQChQE3ACoYnYx');
        
//     client.featuredEvent({
//         location: 'claremont, ca'
//     }).then(response => {
//     console.log(response.jsonBody.description);
//     }).catch(e => {
//         console.log(e);
//     });