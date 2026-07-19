function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

console.log("CSRF Token:", csrftoken);

document.getElementById("contactForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const formData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        desc: document.getElementById("desc").value
    };

    try{

        const response = await fetch("/api/contact/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(formData)
        });

        const data = await response.json();
        // if(response.ok){

        //     document.getElementById("msg").innerHTML=
        //     `<div class="alert alert-success">
        //         ${data.message}
        //     </div>`;

        //     document.getElementById("contactForm").reset();

        // } 
         if (response.ok && data.status) {

    document.getElementById("msg").innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${data.message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    document.getElementById("contactForm").reset();

    // Hide the message after 3 seconds
    setTimeout(() => {
        document.getElementById("msg").innerHTML = "";
    }, 3000);
}
        else{

            document.getElementById("msg").innerHTML=
            `<div class="alert alert-danger">
                Failed to save data.
            </div>`;
        console.log(data);
        }
    }
    catch(error){

        console.log(error);

        document.getElementById("msg").innerHTML=
        `<div class="alert alert-danger">
            Server Error
        </div>`;

    }
});
    
