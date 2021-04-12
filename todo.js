// wait for the page to load

document.addEventListener('DOMContentLoaded', function() {
	//select the input button and input to be user later
	const submit = document.querySelector('#submit');
	const newTask = document.querySelector('#task');
	
	//disable submit button by default
	submit.disabled = true;
	
	//listen for input to be typed into the input field
	newTask.onkeyup = () => {
		if(newTask.value.length>0) {
			submit.disabled = false;
		}
		else {
			submit.disabled = true;
		}
		
	}
	
	//listen for submission of forms
	
	document.querySelector('form').onsubmit = () => {
		
		
		//find the task the user just submitted
		const task = newTask.value;
		
		//create a lsit item for the new task and add the task to it
		const li = document.createElement('li');
		li.innerHTML = task;
		
		//Add new element to our uordered list ;
		document.querySelector('#tasks').append(li);
		
		//clear out input field
		newTask.value = '';
		
		//disable the submit button
		submit.disabled = true;
		
		//stop form from submitting
		return false;
	}
});
