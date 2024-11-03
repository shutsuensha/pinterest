async function fetchUserData() {
    try {
        const response = await fetch(`http://127.0.0.1:8000/users/username/${username}`);

        if (response.status == 200) {
            const userData = await response.json();

            const emailElement = document.createElement("p");
            emailElement.textContent = `Email: ${userData.email}`;
            
            const usernameElement = document.createElement("p");
            usernameElement.textContent = `Username: ${userData.username}`;
            
            // Append these elements to the body or a specific container
            document.body.appendChild(emailElement);
            document.body.appendChild(usernameElement);

            // Fetch the profile image
            const imageResponse = await fetch("http://127.0.0.1:8000/users/files/" + userData.profile);
            if (imageResponse.status == 200) {
                const blob = await imageResponse.blob();

                // Create a URL for the Blob and set it as the image source
                const imageUrl = URL.createObjectURL(blob);

                // Create an <img> element
                const img = document.createElement("img");
                img.src = imageUrl;
                img.alt = "User Profile Image";
                img.width = 200; // Optional: Set width/height or any other styling
                img.height = 200;

                // Append the <img> element to the body or any specific container
                document.body.appendChild(img);
            } else {
                console.error("Failed to fetch the image:", imageResponse.status, imageResponse.statusText);
            }

            for (const pin of userData.pins) {
                const pinElement = document.createElement("div");
                pinElement.classList.add("pin");
        
                // Add title and description
                const title = document.createElement("h3");
                title.textContent = pin.title;
                const description = document.createElement("p");
                description.textContent = pin.description;
        
        
                // Fetch and display media (image or video)
                const mediaResponse = await fetch(`http://127.0.0.1:8000/pins/files/${pin.media}`);
                const mediaBlob = await mediaResponse.blob();
                const mediaURL = URL.createObjectURL(mediaBlob);
                
                let mediaElement;
                if (pin.media.endsWith(".mp4")) {
                  mediaElement = document.createElement("video");
                  mediaElement.src = mediaURL;
                  mediaElement.controls = true;
                  mediaElement.width = 300;
                } else {
                  mediaElement = document.createElement("img");
                  mediaElement.src = mediaURL;
                  mediaElement.alt = pin.title;
                  mediaElement.width = 300;
                }

                const link = document.createElement("a");
                link.href = `/pin/${pin.uid}`;
                link.style.textDecoration = "none"; // Remove default underline

                pinElement.appendChild(mediaElement);

                link.appendChild(pinElement);
        
                // Add pin element to the body
                document.body.appendChild(link);
            }
        } else {
            const errorData = await response.json();
            console.log("Error data:", errorData);
        }
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
    }
}

fetchUserData();