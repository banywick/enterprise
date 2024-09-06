const submit_button = document.querySelector('.button');
const load_animation = document.querySelector('.load_animation');
const error_load_file = document.querySelector('.error_load_file');
submit_button.addEventListener('click', (event) => {
    // Проверяем, был ли клик реальным (не автоматическим)
    if (event.isTrusted) {
        checkTaskStatus();
        
    }
});

console.log({taskId})
function checkTaskStatus() {
    fetch(`http://192.168.100.200/check_task_status/${taskId}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.status === 'PENDING') {
                console.log('Обработка данных!');
                load_animation.style.display = 'flex'

            }
            if (data.status === 'unknown') {
                console.log('обнулен!');
                clearInterval(intervalId);

            }
            if (data.status === 'FAILURE') {
                console.log('Ошибка загрузки данных!');
                error_load_file.style.display = 'flex'
                load_animation.style.display = 'none'
                clearInterval(intervalId);
            }
            if (data.status === 'SUCCESS') {
                console.log('Задача выполнена!');
                clearInterval(intervalId); // Останавливаем интервал
                window.location.href = "192.168.100.200";
            }
        });
}
const intervalId = setInterval(checkTaskStatus, 1000);

