async function uploadMedia(pinUid, mediaFile) {
    const formData = new FormData();
    formData.append('file', mediaFile);

    try {
        const response = await fetch(`/pins/upload/${pinUid}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Error uploading media');
        }

        const result = await response.json();
        console.log('Media uploaded successfully:', result);
    } catch (error) {
        console.error('Error:', error);
        alert('There was a problem uploading your media.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const pinForm = document.createElement('form');
    pinForm.id = 'pinForm';

    // Title Input
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.name = 'title';
    titleInput.placeholder = 'Enter pin title';
    titleInput.required = true;

    // Description Input
    const descriptionInput = document.createElement('textarea');
    descriptionInput.name = 'description';
    descriptionInput.placeholder = 'Enter pin description';
    descriptionInput.required = true;

    // Media Input
    const mediaInput = document.createElement('input');
    mediaInput.type = 'file';
    mediaInput.name = 'media';
    mediaInput.accept = 'image/*,video/*'; // Accepts images and videos
    mediaInput.required = true;

    // Tags Input
    const tagsInput = document.createElement('input');
    tagsInput.type = 'text';
    tagsInput.name = 'tags';
    tagsInput.placeholder = 'Enter tags separated by commas';
    tagsInput.required = true;

    // Submit Button
    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.textContent = 'Create Pin';

    pinForm.appendChild(titleInput);
    pinForm.appendChild(descriptionInput);
    pinForm.appendChild(mediaInput);
    pinForm.appendChild(tagsInput);
    pinForm.appendChild(submitButton);
    document.body.appendChild(pinForm);

    pinForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission
    
        const formData = new FormData(pinForm);
        const title = formData.get('title');
        const description = formData.get('description');
        const tags = formData.get('tags').split(',').map(tag => tag.trim());
        const mediaFile = formData.get('media');
    
        try {
            // Step 1: Create the pin
            const createPinResponse = await fetch('/pins/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, description }),
            });
    
            if (!createPinResponse.ok) {
                throw new Error('Error creating pin');
            }
    
            const createPinResult = await createPinResponse.json();
            const pinUid = createPinResult.pin.uid; // Get pin UID from response
            console.log('Pin created:', createPinResult);
    
            // Step 2: Upload media
            await uploadMedia(pinUid, mediaFile); // Call the upload function
    
            // Step 3: Add tags
            const addTagsResponse = await fetch(`/tags/${pinUid}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ tags }),
            });
    
            if (!addTagsResponse.ok) {
                throw new Error('Error adding tags');
            }
    
            const addTagsResult = await addTagsResponse.json();
            console.log('Tags added:', addTagsResult);
    
            alert('Pin created successfully with media and tags!');
            pinForm.reset(); // Reset the form after successful submission
        } catch (error) {
            console.error('Error:', error);
            alert('There was a problem creating your pin.');
        }
    });
});
