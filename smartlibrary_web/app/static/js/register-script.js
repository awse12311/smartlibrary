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
    document.getElementById('preview-heading').style.display = 'block';
    photo.style.display = 'block';
}


function register() {
    // 獲取註冊信息
    var newEmail = document.getElementById('new-email').value;
    var newUsername = document.getElementById('new-username').value;
    var newPassword = document.getElementById('new-password').value;

    // 檢查表單是否填寫完整
    if (!newEmail || !newUsername || !newPassword) {
        alert('請填寫所有欄位！');
        return;
    }

    // 驗證電子郵件地址的格式
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(newEmail)) {
        alert('請填寫正確的電子郵件地址！');
        return;
    }

    // 獲取勾選的書籍類型
    var bookTypes = [];
    var checkboxes = document.getElementsByName('book-type');
    var atLeastOneChecked = false; // 添加變量來檢查是否至少有一個書籍類型被勾選
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            atLeastOneChecked = true; // 如果有勾選的書籍類型，則將變量設置為 true
            bookTypes.push(checkbox.value);
        }
    });

    // 檢查是否至少有一項書籍類型被勾選
    if (!atLeastOneChecked) {
        alert('請至少選擇一項書籍類型！');
        return;
    }

    // 構造要發送到後端的 JSON 數據
    var data = {
        "email": newEmail,
        "username": newUsername,
        "password": newPassword,
        "bookTypes": bookTypes
    };

    // 發送 POST 請求到後端
    fetch('/registe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // 處理成功響應
            console.log('successfully')
        } else {
            console.error('Failed');
        }
    })
    .then(data => {
        // 處理後端返回的數據
        console.log(data);
        alert('註冊成功！'); // 這裡您可以根據後端返回的數據執行不同的操作
        window.location.href = '/'; // 註冊成功後重定向到登錄頁面
    })
    .catch(error => {
        // 處理錯誤
        console.error('註冊失敗:', error);
        alert('註冊失敗，請稍後重試。');
    });
}
