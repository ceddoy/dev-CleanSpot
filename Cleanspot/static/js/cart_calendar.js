let monthNow = parseInt(new Date().getMonth(), 10) + 1
let yearNow = String(new Date().getFullYear());
let pathCalendar = `/cart/calendar/${yearNow}/${monthNow}/`;

function getAndInsertCalendar(path) {
    fetch(path)
        .then((response) => {
            return response.text();
        })
        .then((data) => {
            document.getElementById('id-calendar-table').innerHTML = data;
        })
        .then((data) => {
            let table_td = document.querySelectorAll('.calendar td')
            for (let i = 0; i < table_td.length; i++) {
                table_td[i].addEventListener('click', function () {
                    for (let j = 0; j < table_td.length; j++) {
                        table_td[j].classList.remove('active');
                    }
                    table_td[i].classList.add('active');
                });
            }
        })
}

getAndInsertCalendar(pathCalendar);

function monthText(monthNow) {
    if (monthNow === 12) monthNow = 'Декабрь'
    if (monthNow === 11) monthNow = 'Ноябрь'
    if (monthNow === 10) monthNow = 'Октябрь'
    if (monthNow === 9) monthNow = 'Сентябрь'
    if (monthNow === 8) monthNow = 'Август'
    if (monthNow === 7) monthNow = 'Июль'
    if (monthNow === 6) monthNow = 'Июнь'
    if (monthNow === 5) monthNow = 'Май'
    if (monthNow === 4) monthNow = 'Апрель'
    if (monthNow === 3) monthNow = 'Март'
    if (monthNow === 2) monthNow = 'Февраль'
    if (monthNow === 1) monthNow = 'Январь'
    return monthNow
}

function monthNumber(numberMonth) {
    if (numberMonth === 'Декабрь') numberMonth = 12
    if (numberMonth === 'Ноябрь') numberMonth = 11
    if (numberMonth === 'Октябрь') numberMonth = 10
    if (numberMonth === 'Сентябрь') numberMonth = 9
    if (numberMonth === 'Август') numberMonth = 8
    if (numberMonth === 'Июль') numberMonth = 7
    if (numberMonth === 'Июнь') numberMonth = 6
    if (numberMonth === 'Май') numberMonth = 5
    if (numberMonth === 'Апрель') numberMonth = 4
    if (numberMonth === 'Март') numberMonth = 3
    if (numberMonth === 'Февраль') numberMonth = 2
    if (numberMonth === 'Январь') numberMonth = 1
    return numberMonth
}

document.querySelector('#month').innerHTML = monthText(monthNow);
document.querySelector('#year').innerHTML = yearNow;

function change(step) {
    let monthNow = document.querySelector('#month').textContent;
    monthNow = monthNow.trim()
    let yearNow = Number(document.querySelector('#year').textContent);

    let numberMonth = monthNumber(monthNow) + step
    if (numberMonth < 1) {
        numberMonth = 12;
        yearNow -= 1;
    }
    if (numberMonth > 12) {
        numberMonth = 1;
        yearNow += 1;
    }

    document.querySelector('#month').innerHTML = monthText(numberMonth);
    document.querySelector('#year').innerHTML = String(yearNow);
    let pathCalendar = `/cart/calendar/${yearNow}/${numberMonth}/`;
    getAndInsertCalendar(pathCalendar);
}

let orderButton = document.querySelector('.order-button');
orderButton.addEventListener('click', function () {
    let select_year = document.querySelector('#year').textContent.trim();
    let select_month = document.querySelector('#month').textContent.trim();
    let select_activeDay = document.querySelector('.active').textContent.trim();
    let is_other_date = document.getElementById('id-other-date')
    let date = {
        year: select_year,
        month: monthNumber(select_month),
        day: select_activeDay,
        is_other_date: is_other_date.checked ? '1' : '0',
    };
    fetch(window.location.pathname, {
        method: 'POST',
        body: JSON.stringify(date)
    })
        .then((data) => {
            console.log(data)
            document.location.href = data.url;
        })
})
console.log(window.location.pathname);