// =======================================
// DIVYA AI
// Main JavaScript
// =======================================

// Smooth Scrolling

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
            .scrollIntoView({

                behavior:"smooth"

            });

    });

});


// Navbar Shadow on Scroll

window.addEventListener("scroll",()=>{

    const navbar=document.querySelector(".navbar");

    if(window.scrollY>20){

        navbar.classList.add("shadow");

    }

    else{

        navbar.classList.remove("shadow");

    }

});


// Fade-in Animation

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("show");

}

});

});

document.querySelectorAll(".feature-card").forEach(card=>{

observer.observe(card);

});