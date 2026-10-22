let search =
document.getElementById(
"search"
);


let box =
document.getElementById(
"suggestions"
);



search.addEventListener(
"keyup",
function(){


fetch(
"/jobs/suggestions/?q="
+
search.value
)

.then(
response=>response.json()
)

.then(
data=>{


box.innerHTML="";


data.forEach(
item=>{


box.innerHTML +=
"<p>"
+
item
+
"</p>";

});


});


});