async function fetchPins() {
  const anchor = document.createElement("a");
  anchor.href = "/pin-creation-tool";
  anchor.className = "create-pin-button";
  anchor.textContent = "Create Pin";

  document.body.appendChild(anchor);
  try {
    const pinsResponse = await fetch("http://127.0.0.1:8000/pins/");
    const pins = await pinsResponse.json();

    const pinsContainer = document.createElement("div");
    pinsContainer.classList.add("pins-container"); // Updated class for the floating layout

    for (const pin of pins) {
      const pinElement = document.createElement("div");
      pinElement.classList.add("pin");

      // Create anchor for mediaContainer
      const mediaLink = document.createElement("a");
      mediaLink.href = `/pin/${pin.uid}`; // Link to the specific pin
      mediaLink.classList.add("media-link");
      mediaLink.style.textDecoration = "none"; // Remove underline

      // Media container
      const mediaContainer = document.createElement("div");
      mediaContainer.classList.add("media-container");

      const mediaResponse = await fetch(`http://127.0.0.1:8000/pins/files/${pin.media}`);
      const mediaBlob = await mediaResponse.blob();
      const mediaURL = URL.createObjectURL(mediaBlob);

      let mediaElement;
      if (pin.media.endsWith(".mp4")) {
        mediaElement = document.createElement("video");
        mediaElement.src = mediaURL;
        mediaElement.controls = true;
      } else {
        mediaElement = document.createElement("img");
        mediaElement.src = mediaURL;
        mediaElement.alt = pin.title;
      }
      mediaContainer.appendChild(mediaElement);

      const title = document.createElement("h3");
      title.textContent = pin.title;
      mediaContainer.appendChild(title);

      // Append mediaContainer to the link
      mediaLink.appendChild(mediaContainer);

      // Append the link to pinElement
      pinElement.appendChild(mediaLink);

      // Create anchor for userContainer
      const userLink = document.createElement("a");
      userLink.href = `/${pin.user.username}`; // Link to the user's profile
      userLink.classList.add("user-link");

      // User container
      const userContainer = document.createElement("div");
      userContainer.classList.add("user-container");
      userContainer.style.display = "flex"; // Use flexbox for alignment
      userContainer.style.alignItems = "center"; // Center items vertically

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

      // Append profileImg to the left of username
      userContainer.prepend(profileImg); // Move profileImg before username

      // Append userContainer to the userLink
      userLink.appendChild(userContainer);

      // Append the user link to pinElement
      pinElement.appendChild(userLink);

      // Append each pin to the container
      pinsContainer.appendChild(pinElement);
    }

    // Append pins container to the body
    document.body.appendChild(pinsContainer);
  } catch (error) {
    console.error("Error fetching pins:", error);
  }
}

fetchPins();