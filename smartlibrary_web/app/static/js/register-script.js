let video, photo;

document.addEventListener('DOMContentLoaded', function() {
    video = document.getElementById('camera');
    photo = document.getElementById('photo');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.error('Unable to start Webcam:', error);
        });
});

function takePhoto() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // 將拍攝的圖片顯示在網頁上
    photo.src = canvas.toDataURL('image/png');

    // 顯示 img 元素
    photo.style.display = 'block';
}
