async function fetchPins() {
  try {
    // Fetch all pins
    const pinsResponse = await fetch("http://127.0.0.1:8000/pins/");
    const pins = await pinsResponse.json();

    // Iterate over each pin and fetch related media
    for (const pin of pins) {
      // Create anchor element linking to the pin's detail page
      const link = document.createElement("a");
      link.href = `/pin/${pin.uid}`;
      link.style.textDecoration = "none"; // Remove default underline

      const pinElement = document.createElement("div");
      pinElement.classList.add("pin");

      // Add title and description
      const title = document.createElement("h3");
      title.textContent = pin.title;

      // Add username
      const username = document.createElement("span");
      username.textContent = `Posted by: ${pin.user.username}`;

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

      // Fetch and display profile image
      const profileResponse = await fetch(`http://127.0.0.1:8000/users/files/${pin.user.profile}`);
      const profileBlob = await profileResponse.blob();
      const profileURL = URL.createObjectURL(profileBlob);

      const profileImg = document.createElement("img");
      profileImg.src = profileURL;
      profileImg.alt = `${pin.user.username}'s profile`;
      profileImg.width = 50;
      profileImg.height = 50;

      // Append all elements to the pin container
      pinElement.appendChild(mediaElement);
      pinElement.appendChild(title);

      // Append pin element to the anchor link
      link.appendChild(pinElement);

      const userLink = document.createElement("a");
      userLink.href = `/${pin.user.username}`;
      userLink.appendChild(username)
      userLink.appendChild(profileImg)

      // Add the clickable pin element to the body
      document.body.appendChild(link);
      document.body.appendChild(userLink);
    }
  } catch (error) {
    console.error("Error fetching pins:", error);
  }
}

// Run the function to fetch and display pins
fetchPins();