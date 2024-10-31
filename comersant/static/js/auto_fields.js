const check_article = document.querySelector('.check_article');
const views_title = document.querySelector('.views_title');
const views_article = document.getElementById('hidden_article');
const views_unit = document.getElementById('hidden_unit');




check_article.addEventListener('input', async function () {
    const enteredArticle = check_article.value; 
    // console.log(enteredArticle);

    try {
        if (enteredArticle.trim() === '') {
            // Если в инпуте нет значений, очищаем название
            views_title.value = '';

        } else {
            const response = await fetch(`/check_article/${enteredArticle}`);
            const data = await response.json();
            console.log(data)
              // Отображаем название рядом с инпутом
            if (data.title) {
                views_title.value = data.title;
            }
            if (data.article) {
                views_article.value = data.article;
            }
            if (data.unit) {
                views_unit.value = data.unit;
            }
            if (data.error) {
                views_title.innerHTML = data.error;
            }
        }

    } catch (error) {
        console.error('Ошибка при выполнении fetch-запроса:', error);
    }
});



