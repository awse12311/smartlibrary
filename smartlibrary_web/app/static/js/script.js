document.addEventListener('DOMContentLoaded', function() {
    // Get the video element and set the source to the user's webcam
    const video = document.getElementById('videoInput');

    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.error('Unable to start Webcam:', error);
        });

    // 獲取 canvasOutput 元素
    const canvasOutput = document.getElementById('canvasOutput');

    // 加載 OpenCV.js 並在文檔載入後執行人臉檢測
    cv['onRuntimeInitialized'] = function() {
        console.log('OpenCV.js initialized successfully');
        // 你的 OpenCV.js 人臉檢測代碼
        let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
        let dst = new cv.Mat(video.height, video.width, cv.CV_8UC4);
        let gray = new cv.Mat();
        let cap = new cv.VideoCapture(video);
        let faces = new cv.RectVector();
        let classifier = new cv.CascadeClassifier();
        let minWidth = 100;
        let minHeight = 100;
        let minSize = new cv.Size(minWidth, minHeight);
        let scaleFactor = 1.1;
        let minNeighbors = 3;
        let flags = 0;
        
        // load pre-trained classifiers using utils
        let utils = new Utils('errorMessage');
        let faceCascadeFile = 'haarcascade_frontalface_default.xml';
        utils.createFileFromUrl(faceCascadeFile, '../static/js/haarcascade_frontalface_default.xml', () => {
            classifier.load(faceCascadeFile);
            console.log('classifier loaded');
            // start processing video frames
            const FPS = 30;
            function processVideo() {
                try {
                    // start processing.
                    let begin = Date.now(); // 新增這行以定義 begin 變數
                    cap.read(src);
                    src.copyTo(dst);
                    cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
                    // detect faces.
                    classifier.detectMultiScale(gray, faces, scaleFactor, minNeighbors, flags, minSize);
                    // draw faces.
                    for (let i = 0; i < faces.size(); ++i) {
                        let face = faces.get(i);
                        let point1 = new cv.Point(face.x, face.y);
                        let point2 = new cv.Point(face.x + face.width, face.y + face.height);
                        cv.rectangle(dst, point1, point2, [255, 0, 0, 255]);
                    }
                    cv.imshow('canvasOutput', dst);
                    // schedule the next one.
                    let delay = 1000/FPS - (Date.now() - begin);
                    setTimeout(processVideo, delay);
                } catch (err) {
                    console.error('An error occurred:', err);
                }
            }

            // schedule the first one.
            setTimeout(processVideo, 0);
        });
    };
});

function login() {
    // 取得帳號和密碼
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // 使用 fetch 發送 POST 請求到後端
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => {
        if (response.ok) {
            // 登入成功，可以執行相應的操作
            console.log('Login successful');
            return response.json(); // 返回一個 Promise 對象，解析為 JSON 格式的數據
        } else {
            // 登入失敗，處理錯誤
            console.error('Login failed');
            alert('登入失敗，請確認帳號密碼是否正確')
            throw new Error('登入失敗');
        }
    })
    .then(data => {
        // 在這裡處理從後端返回的 JSON 數據
        if (data.success) {
            console.log(data.user)
            alert('登入成功，請等待頁面跳轉，正在搜尋推薦書籍'); // 在這裡添加 alert，包含成功登入的用戶名
            window.location.href = '/user/' +  data.user.user_id; // 如果有需要，可以重定向到用戶首頁或其他頁面
        } else {
            alert('登入失敗: ' + data.user); // 在這裡添加 alert，包含登入失敗的原因
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function face_login() {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // 確保 video 元素的 videoWidth 和 videoHeight 屬性已經設置
    if (video.videoWidth > 0 && video.videoHeight > 0) {
        // 設置 canvas 寬度和高度等於 video 寬度和高度
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // 將 video 幀繪製到 canvas 上
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 將 canvas 圖像轉換為 base64 格式
        const imageData = canvas.toDataURL('image/png');

        // 使用 fetch 將圖像數據發送到後端
        fetch('/save_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => {
            if (response.ok) {
                console.log('Image saved successfully');
            } else {
                console.error('Failed to save image');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

        fetch('/login_face', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (response.ok) {
                // 登入成功，可以執行相應的操作
                console.log('Login successful');
                return response.json(); // 返回一個 Promise 對象，解析為 JSON 格式的數據
            } else {
                // 登入失敗，處理錯誤
                console.error('Login failed');
                alert('登入失敗，請再試一次或使用帳號密碼登入')
                throw new Error('登入失敗');
            }
        })

        .then(data => {
            // 在這裡處理從後端返回的 JSON 數據
            if (data.success) {
                console.log(data.user)
                console.log(data.recommend_book)
                alert('登入成功，請等待頁面跳轉，正在搜尋推薦書籍'); // 在這裡添加 alert，包含成功登入的用戶名
                window.location.href = '/user/' +  data.user; // 如果有需要，可以重定向到用戶首頁或其他頁面
            } else {
                alert('登入失敗，請再試一次或使用帳號密碼登入 '); // 在這裡添加 alert，包含登入失敗的原因
            }
        })

        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.error('Video metadata not loaded yet');
    }

    
}

document.addEventListener('DOMContentLoaded', function() {
    // 獲取 video 元素並設置其來源為用戶的攝像頭
    video = document.getElementById('videoInput');

    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error('Unable to start Webcam:', error);
        });

    // 綁定 face_login 函數到按鈕的點擊事件
    const faceLoginButton = document.getElementById('faceLoginButton');
    if (faceLoginButton) {
        faceLoginButton.addEventListener('click', face_login);
    }

    // 確保 video 元素的元數已經加載完畢
    video.addEventListener('loadedmetadata', function() {
        console.log('Video metadata loaded');
    });
});
