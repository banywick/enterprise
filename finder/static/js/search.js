const tableRows = document.querySelectorAll('tr[data-id]');
const button_hide = document.querySelector('.button_hide');
const details_div = document.querySelector('.overlay');
button_hide.addEventListener('click', hide_details)

// Добавляем обработчик события для каждой строки
tableRows.forEach((row) => {
    row.addEventListener('click', () => {
        console.log(row);
        // Получаем значение атрибута data-id
        const art = row.getAttribute('data-id');
        details_div.style.display = 'block'
        // Здесь вы можете выполнять дополнительные действия с полученным id
        fetch(`/details/${art}`)
        .then(data=> data.json())
        .then(data => {
            console.log(data)
            document.querySelector(".details_article").textContent = data.art;
            document.querySelector(".details_title").textContent = data.title;
            document.querySelector(".details_sum").textContent =  data.sum;
            document.querySelector(".details_sum_article").textContent = data.sum_art_proj;
            const project_item = document.querySelector('.delails_proj_item'); 
            project_item.innerHTML = "" 
            data.project.forEach((proj) => {
                const listItem = document.createElement("div");
                listItem.textContent = proj;
                project_item.appendChild(listItem)
            
            });
            });
        })});

function hide_details() {
    details_div.style.display = 'none'
}

document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('myTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) { // Начинаем с 1, чтобы пропустить заголовок
        rows[i].addEventListener('click', function() {
            const code = this.querySelector('.code_remains').innerText;
            const title = this.querySelector('.title_remains').innerText;

            const rowText = `${code}\t${title}`;

            navigator.clipboard.writeText(rowText).then(function() {
                rows[i].classList.add('copied');
                console.log('Row copied to clipboard!');
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        });
        rows[i].addEventListener('mouseout', function() {
            this.classList.remove('copied');
        });
    }
});

