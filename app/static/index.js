var page = 1; // Current page number (you can change this dynamically)
var limit = 8;

const pinsContainer = document.createElement("div");
pinsContainer.classList.add("pins-container");

async function fetchPins() {
    // Create and display the loading spinner
    const spinner = createLoadingSpinner();

    // Check for access token in cookies
    const cookies = document.cookie.split(";").map(cookie => cookie.trim());
    const accessToken = cookies.find(cookie => cookie.startsWith("access_token="));

    if (!accessToken) {
        // If no access token, display Login and Signup buttons
        const buttonsContainer = document.createElement("div");
        buttonsContainer.className = "buttons-container"; // Add a container for styling

        const loginButton = document.createElement("a");
        loginButton.href = "/login";
        loginButton.className = "auth-button";
        loginButton.textContent = "Login";

        const signupButton = document.createElement("a");
        signupButton.href = "/signup";
        signupButton.className = "auth-button";
        signupButton.textContent = "Signup";

        // Append buttons to the container
        buttonsContainer.appendChild(loginButton);
        buttonsContainer.appendChild(signupButton);

        // Append the container to the body
        document.body.appendChild(buttonsContainer);

        // Hide the spinner after showing buttons
        spinner.remove();
        return; // Exit the function early
    }

    // If access token exists, display the pins and Create Pin button
    const buttonContainer = document.createElement("div");
    buttonContainer.className = "button-container"; // Add a container for buttons
    buttonContainer.style.textAlign = "center"; // Center align buttons

    const anchor = document.createElement("a");
    anchor.href = "/pin-creation-tool";
    anchor.className = "create-pin-button";
    anchor.textContent = "Create Pin";

    const meButton = document.createElement("a");
    meButton.className = "me-button"; // Add class for styling

    try {
        const meUserResponse = await fetch(`http://127.0.0.1:8000/users/me`);
        const userData = await meUserResponse.json();

        const profileResponse = await fetch(`http://127.0.0.1:8000/users/files/${userData.profile}`);
        const profileBlob = await profileResponse.blob();
        const profileURL = URL.createObjectURL(profileBlob);
        const profileImg = document.createElement("img");
        profileImg.src = profileURL;
        profileImg.alt = `${userData.username}'s profile`;
        profileImg.width = 50;
        profileImg.height = 50;

        const username = document.createElement("span");
        username.textContent = `${userData.username}`;

        const userLink = document.createElement("a");
        userLink.href = `/${userData.username}`;
        userLink.appendChild(username);
        userLink.appendChild(profileImg);
        meButton.appendChild(userLink);

        buttonContainer.appendChild(anchor);
        buttonContainer.appendChild(meButton);
        document.body.appendChild(buttonContainer);

        const pinsResponse = await fetch(`http://127.0.0.1:8000/pins/?page=${page}&limit=${limit}`);
        const pins = await pinsResponse.json();

        for (const pin of pins) {
            const pinElement = document.createElement("div");
            pinElement.classList.add("pin");

            const mediaLink = document.createElement("a");
            mediaLink.href = `/pin/${pin.uid}`;
            mediaLink.classList.add("media-link");
            mediaLink.style.textDecoration = "none";

            const mediaContainer = document.createElement("div");
            mediaContainer.classList.add("media-container");

            const mediaResponse = await fetch(`http://127.0.0.1:8000/pins/files/${pin.media}`);
            const mediaBlob = await mediaResponse.blob();
            const mediaURL = URL.createObjectURL(mediaBlob);

            let mediaElement;
            if (pin.media.endsWith(".mp4")) {
                mediaElement = document.createElement("video");
                mediaElement.src = mediaURL;
                mediaElement.controls = false; // Optionally hide controls for a cleaner look
                mediaElement.autoplay = true; // Autoplay the video
                mediaElement.muted = true; // Mute the video
                mediaElement.loop = true; // Loop the video
            } else {
                mediaElement = document.createElement("img");
                mediaElement.src = mediaURL;
                mediaElement.alt = pin.title;
            }
            mediaContainer.appendChild(mediaElement);

            const title = document.createElement("h3");
            title.textContent = pin.title;
            mediaContainer.appendChild(title);

            mediaLink.appendChild(mediaContainer);
            pinElement.appendChild(mediaLink);

            const userLink = document.createElement("a");
            userLink.href = `/${pin.user.username}`;
            userLink.classList.add("user-link");

            const userContainer = document.createElement("div");
            userContainer.classList.add("user-container");
            userContainer.style.display = "flex";
            userContainer.style.alignItems = "center";

            const username = document.createElement("span");
            username.textContent = `${pin.user.username}`;
            username.classList.add("username");
            userContainer.appendChild(username);

            const profileResponse = await fetch(`http://127.0.0.1:8000/users/files/${pin.user.profile}`);
            const profileBlob = await profileResponse.blob();
            const profileURL = URL.createObjectURL(profileBlob);

            const profileImg = document.createElement("img");
            profileImg.src = profileURL;
            profileImg.alt = `${pin.user.username}'s profile`;
            profileImg.classList.add("profile-img");

            userContainer.prepend(profileImg);
            userLink.appendChild(userContainer);
            pinElement.appendChild(userLink);

            pinsContainer.appendChild(pinElement);
        }

        document.body.appendChild(pinsContainer);
    } catch (error) {
        console.error("Error fetching pins:", error);
    } finally {
        // Remove the spinner after all operations are done
        spinner.remove();
    }

    // Add scroll event listener to check if user has scrolled to the bottom
    window.addEventListener("scroll", async function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            page = page + 1;
            const pinsResponse = await fetch(`http://127.0.0.1:8000/pins/?page=${page}&limit=${limit}`);
            const pins = await pinsResponse.json();

            for (const pin of pins) {
                const pinElement = document.createElement("div");
                pinElement.classList.add("pin");

                const mediaLink = document.createElement("a");
                mediaLink.href = `/pin/${pin.uid}`;
                mediaLink.classList.add("media-link");
                mediaLink.style.textDecoration = "none";

                const mediaContainer = document.createElement("div");
                mediaContainer.classList.add("media-container");

                const mediaResponse = await fetch(`http://127.0.0.1:8000/pins/files/${pin.media}`);
                const mediaBlob = await mediaResponse.blob();
                const mediaURL = URL.createObjectURL(mediaBlob);

                let mediaElement;
                if (pin.media.endsWith(".mp4")) {
                    mediaElement = document.createElement("video");
                    mediaElement.src = mediaURL;
                    mediaElement.controls = false; // Optionally hide controls
                    mediaElement.autoplay = true; // Autoplay the video
                    mediaElement.muted = true; // Mute the video
                    mediaElement.loop = true; // Loop the video
                } else {
                    mediaElement = document.createElement("img");
                    mediaElement.src = mediaURL;
                    mediaElement.alt = pin.title;
                }
                mediaContainer.appendChild(mediaElement);

                const title = document.createElement("h3");
                title.textContent = pin.title;
                mediaContainer.appendChild(title);

                mediaLink.appendChild(mediaContainer);
                pinElement.appendChild(mediaLink);

                const userLink = document.createElement("a");
                userLink.href = `/${pin.user.username}`;
                userLink.classList.add("user-link");

                const userContainer = document.createElement("div");
                userContainer.classList.add("user-container");
                userContainer.style.display = "flex";
                userContainer.style.alignItems = "center";

                const username = document.createElement("span");
                username.textContent = `${pin.user.username}`;
                username.classList.add("username");
                userContainer.appendChild(username);

                const profileResponse = await fetch(`http://127.0.0.1:8000/users/files/${pin.user.profile}`);
                const profileBlob = await profileResponse.blob();
                const profileURL = URL.createObjectURL(profileBlob);

                const profileImg = document.createElement("img");
                profileImg.src = profileURL;
                profileImg.alt = `${pin.user.username}'s profile`;
                profileImg.classList.add("profile-img");

                userContainer.prepend(profileImg);
                userLink.appendChild(userContainer);
                pinElement.appendChild(userLink);

                pinsContainer.appendChild(pinElement);
            }
        }
    });
}

// Function to create and display the loading spinner
function createLoadingSpinner() {
    const spinner = document.createElement("div");
    spinner.className = "loading-spinner";
    document.body.appendChild(spinner);
    return spinner;
}

// Call the function to fetch pins
fetchPins();
