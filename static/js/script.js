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
// =======================================
// ASK DIVYA AI
// =======================================

document.addEventListener("DOMContentLoaded", function () {

    const chatForm =
        document.getElementById("chatForm");

    const chatInput =
        document.getElementById("chatInput");

    const chatMessages =
        document.getElementById("chatMessages");


    // If this isn't the chatbot page,
    // do nothing.

    if (!chatForm || !chatInput || !chatMessages) {
        return;
    }


    chatForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const message =
                chatInput.value.trim();


            if (!message) {
                return;
            }


            // Show user's message

            const userMessage =
                document.createElement("div");

            userMessage.className =
                "user-message";

            userMessage.innerHTML =
                `<p>${message}</p>`;

            chatMessages.appendChild(
                userMessage
            );


            // Clear input

            chatInput.value = "";


            // Scroll to bottom

            chatMessages.scrollTop =
                chatMessages.scrollHeight;


            try {

                const response =
                    await fetch("/ask", {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            message: message

                        })

                    });


                const data =
                    await response.json();


                console.log(
                    "DIVYA RESPONSE:",
                    data
                );


                if (!data.success) {

                    throw new Error(
                        data.message ||
                        "DIVYA could not respond."
                    );

                }


                // Show DIVYA response

                const botMessage =
                    document.createElement("div");

                botMessage.className =
                    "bot-message";


                botMessage.innerHTML = `

                    <strong>DIVYA AI</strong>

                    <p>
                        ${data.response}
                    </p>

                `;


                chatMessages.appendChild(
                    botMessage
                );


                // Scroll to bottom

                chatMessages.scrollTop =
                    chatMessages.scrollHeight;


            } catch (error) {

                console.error(
                    "Chatbot error:",
                    error
                );


                const errorMessage =
                    document.createElement("div");

                errorMessage.className =
                    "bot-message";


                errorMessage.innerHTML = `

                    <strong>DIVYA AI</strong>

                    <p>
                        Sorry, I am unable to respond
                        right now.
                    </p>

                `;


                chatMessages.appendChild(
                    errorMessage
                );

            }

        }
    );

});