
document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('form').onsubmit = function() {
		const name = document.querySelector('#name').value;
		console.log('Hello');
		alert(`Hello, ${name}`);
		console.log('Hello');
	};
	document.querySelectorAll('button').forEach(button => {
		button.onclick = () => {
			document.querySelector("#hello").style.color = button.dataset.color;
			console.log(document.querySelectorAll('button'));
			console.log("hello");
		}
	});
	document.querySelector('select').onchange = function() {
		document.querySelector('#hello').style.color = this.value;
	}
});
