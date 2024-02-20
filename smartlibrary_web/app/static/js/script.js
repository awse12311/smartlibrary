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
                    classifier.detectMultiScale(gray, faces, 1.1, 3, 0);
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
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 使用 fetch 發送 POST 請求到後端
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (response.ok) {
            // 登入成功，可以執行相應的操作
            console.log('Login successful');
            window.location.href = '/user';
        } else {
            // 登入失敗，處理錯誤
            console.error('Login failed');
            return response.json(); // 返回一個 Promise 對象，解析為 JSON 格式的數據
        }
    })
    .then(data => {
        // 在這裡處理從後端返回的 JSON 數據
        if (data) {
            alert('登入失敗: ' + data.user); // 在這裡添加 alert，包含 login_result
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


