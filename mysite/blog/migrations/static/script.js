document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = '{{ csrf_token }}';

    const handleLikeDislike = (postId, action) => {
        fetch(`/posts/${postId}/${action}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.updated_count !== undefined) {
                const counter = document.getElementById(`${action}-count-${postId}`);
                if (counter) {
                    counter.textContent = data.updated_count;
                }
            }
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred.');
        });
    };

    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;
            handleLikeDislike(postId, 'like');
        });
    });

    document.querySelectorAll('.dislike-btn').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.dataset.postId;
            handleLikeDislike(postId, 'dislike');
        });
    });
});
