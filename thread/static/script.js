const tweetText = document.getElementById('tweet-text');
const charRemaining = document.getElementById('char-remaining');
const imageInput = document.getElementById('image-input');
const imagePreview = document.getElementById('image-preview');

tweetText.addEventListener('keyup', () => {
  const textLength = tweetText.value.length;
  const remainingChars = 280 - textLength;

  charRemaining.textContent = remainingChars;

  if (remainingChars < 0) {
    charRemaining.style.color = 'red';
    tweetText.style.borderColor = 'red';
  } else {
    charRemaining.style.color = '#999';
    tweetText.style.borderColor = '#ddd';
  }
});

imageInput.addEventListener('change', function () {
  if (this.files && this.files[0]) {
    const reader = new FileReader();

    reader.onload = function (e) {
      imagePreview.src = e.target.result;
    };

    reader.readAsDataURL(this.files[0]);
  }
});
