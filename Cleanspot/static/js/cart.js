function change(objName, min, max, step) {
    let obj = document.getElementById(objName)
    let tmp = +obj.value + step
    if (tmp < min) tmp = min
    if (tmp > max) tmp = max
    obj.value = tmp
    if (objName === 'amount'){
        document.querySelector('.table-cell__number-staff').innerHTML = tmp
    }
}


function daySchedule(day, number) {
    if (document.getElementsByClassName('lable-checkbox__input')[number].checked) {
        document.querySelector('.table-cell__days-week').innerHTML += ' ' + day
    } else {
        document.querySelector('.table-cell__days-week',).innerHTML = document
            .querySelector('.table-cell__days-week')
            .innerHTML.replace(day, '')
    }
}