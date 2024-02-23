const submit_button = document.querySelector('.button');
const load_animation = document.querySelector('.load_animation');
const error_load_file = document.querySelector('.error_load_file');
submit_button.addEventListener('click', (event) => {
    // Проверяем, был ли клик реальным (не автоматическим)
    if (event.isTrusted) {
        checkTaskStatus();
        
    }
});


function checkTaskStatus() {
    fetch('http://127.0.0.1:8000/check_task_status/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'pending') {
                console.log('Обработка данных!');
                load_animation.style.display = 'flex'

            }
            if (data.status === 'unknown') {
                console.log('обнулен!');
                clearInterval(intervalId);

            }
            if (data.status === 'failure') {
                console.log('Ошибка загрузки данных!');
                error_load_file.style.display = 'flex'
                load_animation.style.display = 'none'
                clearInterval(intervalId);
            }
            if (data.status === 'success') {
                console.log('Задача выполнена!');
                clearInterval(intervalId); // Останавливаем интервал
                window.location.href = "http://127.0.0.1:8000/main/";
            }
        });
}
const intervalId = setInterval(checkTaskStatus, 1000);

