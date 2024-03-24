
allStories = {
	{
		id: "0",
		author: "Author",
		imageUrl: imageurl,

	}
}
const stories = document.querySelector(".stories");
const storiesFullView = document.querySelector(".stories-full-view");
const closeBtn = document.querySelector(".close-btn");

const createStories = () {
	allStories.forEach(s => {
		const story = document.createElement("div");
		story.classList.add("story");
		const img = document.createElement("img");
		img.src = s.imageUrl;
		const author = document.createElement("div");
		author.classList.add("author");
		author.innerHTML = s.author;

		story.appendChild(img);
		story.appendChild(author);

		stories.appendChild(story);

		story.addEventListener("click", () => {
			showFullView();
		});
	});
};

createstories();

const showFullFullView = () => {
	storiesFullView.classList.add("active");
};

closeBtn.addEventListener("click", () => {
	storiesFullView.classList.remove("active");

});
