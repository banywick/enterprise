document.getElementById('input_data_form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    console.log(formData)
    fetch("{% url 'input_data' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        }
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const tableBody = document.getElementById('invoiceTableBody');
            const newRow = tableBody.insertRow();
            newRow.insertCell(0).textContent = data.data.invoice;
            newRow.insertCell(1).textContent = data.data.date;
            newRow.insertCell(2).textContent = data.data.supplier;
            newRow.insertCell(3).textContent = data.data.article;
            newRow.insertCell(4).textContent = data.data.auto_title;
            newRow.insertCell(5).textContent = 'шт';  // Пример значения, можно изменить
            newRow.insertCell(6).textContent = data.data.quantity;
            newRow.insertCell(7).textContent = data.data.comment;
            newRow.insertCell(8).textContent = data.data.leading;
        } else {
            alert('Ошибка при отправке данных');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});