document.addEventListener('DOMContentLoaded', function () {
    // -----------------------------
    // Reply Form Script
    // -----------------------------
    const replyLinks = document.querySelectorAll('.comment-reply');
    const replyForm = document.getElementById('reply-form');
    const parentInput = document.getElementById('parent-id');
    let currentParentComment = null;

    replyLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            const commentId = this.getAttribute('data-comment-id');
            const parentComment = this.closest('.comment-meta');

            if (currentParentComment === parentComment) {
                replyForm.style.display = 'none';
                parentInput.value = '';
                currentParentComment = null;
            } else {
                parentInput.value = commentId;
                parentComment.appendChild(replyForm);
                replyForm.style.display = 'block';
                currentParentComment = parentComment;
            }
        });
    });

    // -----------------------------
    // File Upload and Preview Script
    // -----------------------------
    const fileInput = document.getElementById('file-upload');
    const filePreview = document.getElementById('file-preview');
    const imagePreview = document.getElementById('image-preview');
    const textPreview = document.getElementById('text-preview');

    fileInput.addEventListener('change', function () {
        const file = this.files[0];

        filePreview.style.display = 'none';
        imagePreview.style.display = 'none';
        textPreview.style.display = 'none';

        if (!file) return;

        if (file.size > 102400) { // 100 KB
            alert('File size must be less than 100 KB.');
            this.value = '';
            return;
        }

        const fileType = file.type;

        if (fileType.startsWith('image/')) {
            const img = new Image();
            const reader = new FileReader();

            reader.onload = function (e) {
                img.src = e.target.result;

                img.onload = function () {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');

                    let width = img.width;
                    let height = img.height;

                    if (width > 320 || height > 240) {
                        const ratio = Math.min(320 / width, 240 / height);
                        width = Math.round(width * ratio);
                        height = Math.round(height * ratio);
                    }

                    canvas.width = width;
                    canvas.height = height;
                    ctx.drawImage(img, 0, 0, width, height);

                    imagePreview.src = canvas.toDataURL(fileType);
                    imagePreview.style.display = 'block';
                    filePreview.style.display = 'block';
                };
            };

            reader.readAsDataURL(file);
        } else if (fileType === 'text/plain') {
            const reader = new FileReader();

            reader.onload = function (e) {
                textPreview.textContent = e.target.result;
                textPreview.style.display = 'block';
                filePreview.style.display = 'block';
            };

            reader.readAsText(file);
        } else {
            alert('Invalid file type. Only JPG, PNG, GIF, and TXT files are allowed.');
            this.value = '';
        }
        });

    // -----------------------------
    // Comment Preview Script
    // -----------------------------
    const previewButton = document.getElementById('preview-button');
    const previewArea = document.getElementById('preview-area');
    const previewUsername = document.getElementById('preview-username');
    const previewEmail = document.getElementById('preview-email');
    const previewContent = document.getElementById('preview-content');

    previewButton.addEventListener('click', function () {
        const formData = new FormData(document.getElementById('comment-form'));

        fetch("{% url 'preview_message' %}", {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                previewUsername.textContent = `Username: ${data.username}`;
                previewEmail.textContent = `Email: ${data.email}`;
                previewContent.innerHTML = `Message: ${data.text}`;
                previewArea.style.display = 'block';
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });

