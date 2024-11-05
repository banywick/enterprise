document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('inputDataForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload('/shortfalls');
            } else {
                // Ошибка валидации, отобразить ошибки в форме
                for (const field in data.errors) {
                    const errorElement = document.createElement('div');
                    errorElement.classList.add('error');
                    errorElement.textContent = data.errors[field][0];
                    document.querySelector(`#id_${field}`).parentNode.appendChild(errorElement);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});