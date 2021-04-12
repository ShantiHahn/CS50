document.addEventListener('DOMContentLoaded', function() {

	document.querySelector('form').onsubmit = function() {
			//send get request to the url
		fetch('https://api.exchangeratesapi.io/latest?base=USD')
	
		//put response into JSON form
		.then(response => response.json())
		.then(data => {
			//log data to the console
			console.log(data);
			
			const currency = document.querySelector('#currency').value.toUpperCase();
			
			
			//get rate from data
			const rate = data.rates[currency];
			
			//check if currency is valid
			if (rate !== undefined) {
			
				//display exchange on screen
				document.querySelector('body').innerHTML = `1 USD is equal to ${rate.to.fixed(3)} ${currency} .`; 
			}
			else {
			
				//display error message
				document.querySelector("#result").innerHTML = 'Invalid Currency';
			}
			
			//display the message on the screen
			
			
		})
		//catch any errors and log them to the console
		.catch(error => {
			console.log('Error:', error);
			
		});
		//prevent default submission
		return false;
	
	};

});
