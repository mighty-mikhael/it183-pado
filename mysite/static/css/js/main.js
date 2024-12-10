document.addEventListener("DOMContentLoaded", function() {
    const likeButtons = document.querySelectorAll('.like-button');
    const dislikeButtons = document.querySelectorAll('.dislike-button');

    likeButtons.forEach(function(btn) {
        btn.addEventListener("click", function() {
            const postId = btn.id.split('-')[1];  // Extract post ID from the button's ID
            const dislikeBtn = document.querySelector(`#dislike-${postId}`);

            // Toggle like button active class
            btn.classList.toggle("active");

            // If the dislike button is active, remove its active class
            if (dislikeBtn.classList.contains("active")) {
                dislikeBtn.classList.remove("active");
            }

            // You can also trigger an AJAX call here to update like/dislike status on the backend
            updateLikes(postId, btn.classList.contains("active"));
        });
    });

    dislikeButtons.forEach(function(btn) {
        btn.addEventListener("click", function() {
            const postId = btn.id.split('-')[1];  // Extract post ID from the button's ID
            const likeBtn = document.querySelector(`#like-${postId}`);

            // Toggle dislike button active class
            btn.classList.toggle("active");

            // If the like button is active, remove its active class
            if (likeBtn.classList.contains("active")) {
                likeBtn.classList.remove("active");
            }

            // You can also trigger an AJAX call here to update like/dislike status on the backend
            updateDislikes(postId, btn.classList.contains("active"));
        });
    });

    // AJAX call to update the like status on the backend
    function updateLikes(postId, isLiked) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: `/posts/${postId}/like/`,  // Adjust URL to your actual endpoint
            type: 'POST',
            data: {
                'liked': isLiked,
                'csrfmiddlewaretoken': csrfToken,  // Include CSRF token
            },
            success: function(response) {
                // Handle success (update like count, etc.)
            },
            error: function(error) {
                console.error("Error updating like:", error);
            }
        });
    }

    // AJAX call to update the dislike status on the backend
    function updateDislikes(postId, isDisliked) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: `/posts/${postId}/dislike/`,  // Adjust URL to your actual endpoint
            type: 'POST',
            data: {
                'disliked': isDisliked,
                'csrfmiddlewaretoken': csrfToken,  // Include CSRF token
            },
            success: function(response) {
                // Handle success (update dislike count, etc.)
            },
            error: function(error) {
                console.error("Error updating dislike:", error);
            }
        });
    }
});
