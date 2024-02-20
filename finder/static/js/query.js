const submit_button = document.querySelector('.button')
submit_button.addEventListener('click', checkTaskStatus)


function checkTaskStatus() {
  
    fetch('http://127.0.0.1:8000/check_task_status/')
        .then(response => response.json())
        .then(data => {
            console.log(data.status)})}

// intervalId = setInterval(checkTaskStatus, 1000);    