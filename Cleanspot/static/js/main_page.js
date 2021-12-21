function insertUrl(path) {
    const orderForm = document.getElementById('main_page_order_form');
    orderForm.action = path;
}

document.addEventListener('DOMContentLoaded', async function () {
    fetch('/main_order/private_person/supporting/')
        .then((response) => {
            return response.text();
        })
        .then((data) => {
            document.getElementById('order').innerHTML = data;
        })
        .then((data) => {
            insertUrl('/main_order/private_person/supporting/');
        });
})

function getHtml(path) {
    fetch(path)
        .then((response) => {
            return response.text();
        })
        .then((data) => {
            document.getElementById('order').innerHTML = data;
        })
        .then((data) => {
            insertUrl(path);
        });
}