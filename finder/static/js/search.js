const tableRows = document.querySelectorAll('tr[data-id]');
const button_hide = document.querySelector('.button_hide');
const details_div = document.querySelector('.overlay');
button_hide.addEventListener('click', hide_details)

// Добавляем обработчик события для каждой строки
tableRows.forEach((row) => {
    row.addEventListener('click', () => {
        // Получаем значение атрибута data-id
        const id = row.getAttribute('data-id');
        details_div.style.display = 'block'
        // Здесь вы можете выполнять дополнительные действия с полученным id
        fetch(`http://10.10.44.4:80/details/${id}`)
        .then(data=> data.json())
        .then(data => {
            console.log(data)
            document.querySelector(".details_article").textContent = data.art;
            document.querySelector(".details_title").textContent = data.title;
            document.querySelector(".details_sum").textContent = data.sum;
            const project_item = document.querySelector('.delails_proj_item'); 
            project_item.innerHTML = "" 
          
            data.project.forEach((proj) => {
               
                const listItem = document.createElement("div");
                console.log(listItem)
                listItem.textContent = proj;
                project_item.appendChild(listItem)
            
            });
            });
        })});

function hide_details() {
    details_div.style.display = 'none'
}



