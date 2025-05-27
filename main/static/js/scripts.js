// Пример простой анимации
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelector('.nav-link.active')?.classList.remove('active');
        this.classList.add('active');
    });
});

// main/static/js/scripts.js

document.getElementById('contrast-mode').addEventListener('click', function () {
    console.log('Кнопка контрастности нажата');
    document.body.classList.toggle('contrast-mode');
});