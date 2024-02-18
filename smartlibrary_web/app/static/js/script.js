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
                console.log('Processing video frame');
                try {
                    // start processing.
                    let begin = Date.now(); // 新增這行以定義 begin 變數
                    cap.read(src);
                    src.copyTo(dst);
                    cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
                    console.log('src,dst ok');
                    // detect faces.
                    classifier.detectMultiScale(gray, faces, 1.1, 3, 0);
                    console.log('detect faces ok');
                    // draw faces.
                    for (let i = 0; i < faces.size(); ++i) {
                        let face = faces.get(i);
                        let point1 = new cv.Point(face.x, face.y);
                        let point2 = new cv.Point(face.x + face.width, face.y + face.height);
                        cv.rectangle(dst, point1, point2, [255, 0, 0, 255]);
                    }
                    console.log('draw faces');
                    cv.imshow('canvasOutput', dst);
                    console.log('imshow');
                    // schedule the next one.
                    let delay = 1000/FPS - (Date.now() - begin);
                    console.log('delay');
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
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Add your login logic here
    console.log('Login clicked. Username:', username, 'Password:', password);
}
