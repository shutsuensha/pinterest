async function fetchPin() {
    try {
      // Fetch all pins
      const response = await fetch(`http://127.0.0.1:8000/pins/${pinUid}`);
      const pin = await response.json();
  
      
      const pinElement = document.createElement("div");
      pinElement.classList.add("pin");
      
      // Add title and description
      const title = document.createElement("h3");
      title.textContent = pin.title;
      const description = document.createElement("p");
      description.textContent = pin.description;
      
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
      pinElement.appendChild(description);
  
      document.body.appendChild(pinElement);

      const userLink = document.createElement("a");
      userLink.href = `/${pin.user.username}`;
      userLink.appendChild(username)
      userLink.appendChild(profileImg)

      // Add the clickable pin element to the body
      document.body.appendChild(userLink);

      if (pin.comments && pin.comments.length > 0) {


        const commentsSection = document.createElement("div");
        commentsSection.classList.add("comments-section");

        const commentsHeader = document.createElement("h2");
        commentsHeader.textContent = "Comments";

        commentsSection.appendChild(commentsHeader);

        for (const comment of pin.comments) {
            const commentContainer = document.createElement("div");
            commentContainer.classList.add("comment");
            const commentUserResponse = await fetch(`http://127.0.0.1:8000/users/uid/${comment.user_uid}`);
            const commentUserData = await commentUserResponse.json();
            const commentUsername = document.createElement("span");
            commentUsername.textContent = commentUserData.username;
            const commentProfileResponse = await fetch(`http://127.0.0.1:8000/users/files/${commentUserData.profile}`);
            const commentProfileBlob = await commentProfileResponse.blob();
            const commentProfileURL = URL.createObjectURL(commentProfileBlob);
            const commentProfileImg = document.createElement("img");
            commentProfileImg.src = commentProfileURL;
            commentProfileImg.alt = `${commentUserData.username}'s profile`;
            commentProfileImg.width = 30;
            commentProfileImg.height = 30;
            const commentText = document.createElement("p");
            commentText.textContent = comment.text;

            const userLink = document.createElement("a");
            userLink.href = `/${commentUserData.username}`;
            userLink.appendChild(commentUsername)
            userLink.appendChild(commentProfileImg)


            commentContainer.appendChild(userLink);
            commentContainer.appendChild(commentText);
            commentsSection.appendChild(commentContainer);
        }
        document.body.appendChild(commentsSection);
      }


      const hr = document.createElement("hr");
      document.body.appendChild(hr);

      const realted = document.createElement("h1");
      realted.textContent = 'Related';
      document.body.appendChild(realted);

      const displayedPins = new Set();
      
      for (const tag of pin.tags) {
        const tagPinsResponse = await fetch(`http://127.0.0.1:8000/tags/${tag.uid}/pins`);
        const tagPins = await tagPinsResponse.json();

        // Display each pin associated with the tag
        for (const tagPin of tagPins) {
            if (displayedPins.has(tagPin.uid) || tagPin.uid === pinUid) {
              continue;
            }

            displayedPins.add(tagPin.uid);


            const link = document.createElement("a");
            link.href = `/pin/${tagPin.uid}`;
            link.style.textDecoration = "none"; // Remove default underline
      
            const pinElement = document.createElement("div");
            pinElement.classList.add("pin");
      
            // Add title and description
            const title = document.createElement("h3");
            title.textContent = tagPin.title;
            const description = document.createElement("p");
            description.textContent = tagPin.description;
      
            // Add username
            const userResponse = await fetch(`http://127.0.0.1:8000/users/uid/${tagPin.user_uid}`);
            const userData = await userResponse.json();


            const username = document.createElement("span");
            username.textContent = `Posted by: ${userData.username}`;
      
            // Fetch and display media (image or video)
            const mediaResponse = await fetch(`http://127.0.0.1:8000/pins/files/${tagPin.media}`);
            const mediaBlob = await mediaResponse.blob();
            const mediaURL = URL.createObjectURL(mediaBlob);
      
            let mediaElement;
            if (tagPin.media.endsWith(".mp4")) {
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
            const profileResponse = await fetch(`http://127.0.0.1:8000/users/files/${userData.profile}`);
            const profileBlob = await profileResponse.blob();
            const profileURL = URL.createObjectURL(profileBlob);
      
            const profileImg = document.createElement("img");
            profileImg.src = profileURL;
            profileImg.alt = `${userData.username}'s profile`;
            profileImg.width = 50;
            profileImg.height = 50;
      
            // Append all elements to the pin container
            pinElement.appendChild(mediaElement);
            pinElement.appendChild(title);
      
            // Append pin element to the anchor link
            link.appendChild(pinElement);

            const userLink = document.createElement("a");
            userLink.href = `/${userData.username}`;
            userLink.appendChild(username)
            userLink.appendChild(profileImg)
      
            // Add the clickable pin element to the body
            document.body.appendChild(link);
            document.body.appendChild(userLink);
          }
        }
        




    
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
    }
}
  
  // Run the function to fetch and display pins
fetchPin();