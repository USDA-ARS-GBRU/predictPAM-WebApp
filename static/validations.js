function ValidationEvent() {
// Storing Field Values In Variables
var pamseq = document.getElementById("pamseq").value;
var targetLength = document.getElementById("targetLength").value;
var lcp = document.getElementById("lcp").value;

// Conditions
	if (lcp > 0.5*targetLength){
		alert("Lcp should not be greater than 50% of Target Length");
		print("I am here")
		return false;
	}
	else {
		return true;
	}
}