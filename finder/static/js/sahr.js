const check_article = document.querySelector('.check_article');
const views_title = document.querySelector('.views_title');
const write_address = document.querySelector('.write_address');
const save_button = document.querySelector('.save_button');
const hidden_id = document.querySelector('.hidden_id');

check_article.addEventListener('input', async function () {
    const enteredArticle = check_article.value; 
    // console.log(enteredArticle);

    try {
        if (enteredArticle.trim() === '') {
            // Если в инпуте нет значений, очищаем название
            views_title.innerHTML = '';
        } else {
            const response = await fetch(`http://127.0.0.1:8000/check_article/${enteredArticle}`);
            const data = await response.json();
            console.log(data.id)
        
            // Отображаем название рядом с инпутом
            if (data.title) {
                views_title.value = data.title;
                hidden_id.value = data.id;
                write_address.style.display = 'block'
                save_button.style.display = 'block'
            }
            if (data.error) {
                views_title.innerHTML = data.error;
            }
        }
    } catch (error) {
        console.error('Ошибка при выполнении fetch-запроса:', error);
    }
});





// const input = document.querySelector('#articleInput');
// const articleName = document.querySelector('#articleName');

// input.addEventListener('input', async function () {
//   const enteredArticle = input.value;

//   try {
//     const response = await fetch(`/check-article/${enteredArticle}`);
//     const data = await response.json();

//     // Отображаем название рядом с инпутом
//     articleName.textContent = data.articleName;
//   } catch (error) {
//     console.error('Ошибка при выполнении fetch-запроса:', error);
//   }
// });