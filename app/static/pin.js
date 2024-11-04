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
      userLink.classList.add("user-link");


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
            if (comment.media) {
              const profileResponse = await fetch(`http://127.0.0.1:8000/comment/files/${comment.media}`);
              const profileBlob = await profileResponse.blob();
              const profileURL = URL.createObjectURL(profileBlob);
          
              const profileImg23 = document.createElement("img");
              profileImg23.src = profileURL;
              profileImg23.alt = 'comment media';
              profileImg23.width = 50;
              profileImg23.height = 50;
              commentContainer.appendChild(profileImg23)
            }


            const repliesResponse = await fetch(`http://127.0.0.1:8000/comment/reply/${comment.uid}`);
            const repliesData = await repliesResponse.json();

            if (repliesData && repliesData.length > 0) {
              for (const reply of repliesData) {
                const replyContainer = document.createElement("div");
                replyContainer.classList.add("reply");
                const replyUserResponse = await fetch(`http://127.0.0.1:8000/users/uid/${reply.user_uid}`);
                const replyUserData = await replyUserResponse.json();
                const replyUsername = document.createElement("span");
                replyUsername.textContent = replyUserData.username;
                const replyProfileResponse = await fetch(`http://127.0.0.1:8000/users/files/${replyUserData.profile}`);
                const replyProfileBlob = await replyProfileResponse.blob();
                const replyProfileURL = URL.createObjectURL(replyProfileBlob);
                const replyProfileImg = document.createElement("img");
                replyProfileImg.src = replyProfileURL;
                replyProfileImg.alt = `${replyUserData.username}'s profile`;
                replyProfileImg.width = 30;
                replyProfileImg.height = 30;
                const replyText = document.createElement("p");
                replyText.textContent = reply.text;
                const userLink = document.createElement("a");
                userLink.href = `/${replyUserData.username}`;
                userLink.appendChild(replyUsername)
                userLink.appendChild(replyProfileImg)

                replyContainer.appendChild(userLink)
                replyContainer.appendChild(replyText)

                if (reply.media) {
                  const profileResponse1 = await fetch(`http://127.0.0.1:8000/comment/files/${reply.media}`);
                  const profileBlob1 = await profileResponse1.blob();
                  const profileURL1 = URL.createObjectURL(profileBlob1);
              
                  const profileImg1 = document.createElement("img");
                  profileImg1.src = profileURL1;
                  profileImg1.alt = 'comment media';
                  profileImg1.width = 50;
                  profileImg1.height = 50;
                  replyContainer.appendChild(profileImg1)
                }

                commentContainer.appendChild(replyContainer)  
              }
            }



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