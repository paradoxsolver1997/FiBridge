document.addEventListener('DOMContentLoaded', function() {
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.style.display = 'none';
    const sendPhotosBtn = document.getElementById('send-photos');
    const photoInput = document.getElementById('photo-input');
    const photoPreviewList = document.getElementById('photo-preview-list');

    sendPhotosBtn.addEventListener('click', function() {
        photoInput.click();
    });

    let selectedFiles = [];
    photoInput.addEventListener('change', function() {
        selectedFiles = Array.from(photoInput.files);
        if (selectedFiles.length) {
            sendBtn.style.display = 'inline-block';
        } else {
            sendBtn.style.display = 'none';
        }
        photoPreviewList.innerHTML = '';
        selectedFiles.forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.className = 'd-inline-block m-2';
                div.innerHTML = `<img src="${e.target.result}" style="max-width:100px;max-height:100px;display:block;"><div>${file.name}</div>`;
                photoPreviewList.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    });

    sendBtn.addEventListener('click', function() {
        if (!selectedFiles.length) {
            alert('Please select files to send');
            return;
        }
        uploadPhotos(selectedFiles);
    });

    function uploadPhotos(files) {
        const formData = new FormData();
        files.forEach(f => formData.append('photos', f));
        fetch('/api/file_share/upload', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('Upload successful!');
            } else {
                alert('Upload failed: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(() => alert('Upload failed, please try again!'));
    }
});