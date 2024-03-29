const check_article = document.querySelector('.check_article');
const views_title = document.querySelector('.views_title');
const write_address = document.querySelector('.write_address');
const save_button = document.querySelector('.save_button');
const hidden_id = document.querySelector('.hidden_id');
const selectElement = document.querySelector('.selectElement');
const tableRowsSahr = document.querySelectorAll('tr[data-id]');
// const chenge_button = document.querySelectorAll('.change_button');
const change_party_info = document.querySelector('.change_party_info');
const change_article_info = document.querySelector('.change_article_info');
const form_id_data_table = document.querySelector('.form_id_data_table');


tableRowsSahr.forEach((row) => {
    row.addEventListener('click', () => {
        // Получаем значение атрибута data-id
        const art = row.getAttribute('data-id');
        const cells = row.getElementsByTagName('td');

        const change_button = row.querySelector('.change_button');
        change_button.addEventListener('click', () => {
        form_id_data_table.innerHTML = cells[0].textContent
        change_party_info.innerHTML = cells[1].textContent
        change_article_info.innerHTML = cells[2].textContent
        console.log(cells[0].textContent);
        console.log(cells[1].textContent);
        console.log(cells[2].textContent);
    });
      



        fetch(`http://127.0.0.1:8000/details/${art}`)
        .then(data=> data.json())
        .then(data => {
            // console.log(data)
            document.querySelector(".sahr_details_article").textContent = data.art;
            document.querySelector(".sahr_details_sum").textContent = data.sum;
    })})})



check_article.addEventListener('input', async function () {
    const enteredArticle = check_article.value; 
    console.log(enteredArticle);

    try {
        if (enteredArticle.trim() === '') {
            // Если в инпуте нет значений, очищаем название
            views_title.value = '';
            selectElement.innerHTML= '';

        } else {
            const response = await fetch(`http://127.0.0.1:8000/check_article/${enteredArticle}`);
            const data = await response.json();
            // console.log(data)
            
            selectElement.innerHTML= ''
            for ( let i in data.party) {
                const option = document.createElement('option');
               ;
                console.log(data.party[i]);
                option.value = data.party[i];
                option.text = data.party[i];
                selectElement.appendChild(option);
            }
            // Отображаем название рядом с инпутом
            if (data.title) {
                views_title.value = data.title;
                hidden_id.value = data.id;
               
            }
            if (data.error) {
                views_title.innerHTML = data.error;
            }
        

        }

    } catch (error) {
        console.error('Ошибка при выполнении fetch-запроса:', error);
    }
});



