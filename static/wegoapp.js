const plan_type = document.querySelector("#plan_type").value
const queryString = new URLSearchParams({'num_people': num_people, 'location': location, 
'budget': budget, 'date': date, 'plan_type': plan_type})
const url = `/user/search?${queryString}`

fetch(url)
	.then(response => response.json())
	.then(response => console.log(response))
	.catch(err => console.error(err));


