function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Add your login logic here
    console.log('Login clicked. Username:', username, 'Password:', password);
}
document.addEventListener('DOMContentLoaded', function() {
    // 找到按鈕元素
    var registerLink = document.getElementById('register-link');

    // 添加點擊事件監聽器
    registerLink.addEventListener('click', function() {
        // 這裡可以加入一些關閉視頻流的邏輯，或其他你需要的操作

        // 然後轉到註冊路由
        window.location.href = "{{ url_for('routes.register') }}";
    });
});