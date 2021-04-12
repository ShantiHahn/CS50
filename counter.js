

    	//check if there is already a value in local storage
    	
    	if(!localStorage.getItem('counter')) {
    	
    	//if not, set the counter to 0 in local storage
    	localStorage.setItem('counter', 0);
    	}



    	count = () => {
    	
    		// retrieve counter value from local storage
    		
    		let counter = localStorage.getItem('counter');
    		
    		//update counter
    		
    		counter++
    		document.querySelector('h1').innerHTML = counter;
    		localStorage.setItem('counter',counter);
    		
    		if (counter % 10 === 0) {
    			alert(`Count is now ${counter}`)
    		}
    		
    	}
    	
    	
    	document.addEventListener('DOMContentLoaded', function() {
    	
    		//set heading to the current value inside local storage
    		document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    		document.querySelector('button').onclick = count;
    		
    	});
    	
    	setInterval(count, 1000);
    	
    	hello = () => {
    		const header = document.querySelector('h1');
    		if (header.innerHTML === 'Hello!') {
    			header.innerHTML = 'Goodbye!';
    			
    		}
    		else {
    			header.innerHTML = 'Hello!';
    		}
    		
    	}
    	

