    // Post a new story 
    const storyForm = document.getElementById('storyform');

    storyForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevents default form submission

        const formData = new FormData(storyForm); // construcs form data

        try {
            const response =  await fetch('/story', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            const key = Object.keys(data);
            // handle responses
            if (key[0] == 'authorImage') {
                const parentDiv = document.getElementById("statusDiv"); // story parent div

                //new child div to house the new story
                const childDIv = document.createElement("div");
                childDIv.className = "story";
                childDIv.style.background = `url('${data.storyImage}')`;
                childDIv.style.backgroundSize = "cover";
                childDIv.style.backgroundRepeat= "no-repeat";
                childDIv.style.backgroundPosition = "center cover";
                
                // div for the story author profile
                const profilePicsDiv =  document.createElement("div");
                profilePicsDiv.className = "profile-pics";
                const profileImage = document.createElement("img");
                profileImage.alt = "ProfilePics";
                profileImage.src = `${data.authorImage}`;
                profilePicsDiv.appendChild(profileImage); // add above image to the div

                // Author username Paragraph
                const authorUsername = document.createElement("p");
                authorUsername.className = "name";
                authorUsername.style.backgroundColor = "black";
                authorUsername.style.color = "white";
                authorUsername.textContent = `${data.authorUsername}`;

                // Story Caption div 
                const captionDiv = document.createElement("div");
                captionDiv.className = "author";
                captionDiv.style.color = "black";
                captionDiv.style.font = "bold";
                captionDiv.textContent = `${data.storyCaption}`;

                // Add all the above to the childDIv
                childDIv.appendChild(profilePicsDiv);
                childDIv.appendChild(authorUsername);
                childDIv.appendChild(captionDiv);

                //Apend childdiv at the beginning of the parentDiv
                parentDiv.prepend(childDIv);

            }
            
        } catch (error) {
            alert('Sever error');
        }

        storyForm.reset();
    });

