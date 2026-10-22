const button =
document.getElementById("theme-toggle");


if (button) {
    button.onclick = function(){


    document.body.classList.toggle(
    "dark"
    );



    if(
    document.body.classList.contains("dark")
    ){

    localStorage.setItem(
    "theme",
    "dark"
    );

    button.innerHTML =
    "☀️";


    }

    else{


    localStorage.setItem(
    "theme",
    "light"
    );


    button.innerHTML =
    "🌙";


    }


    };
}



if(
localStorage.getItem("theme")
==="dark"
){

document.body.classList.add(
"dark"
);


}