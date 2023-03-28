'use strict'


function start-button() {
    // получаем значение поля key
    var keyBox = document.search.key;
    var val = keyBox.value;
    if(val.length>5){
        alert("Недопустимая длина строки");
        e.preventDefault();
    }
    else
        alert("Отправка разрешена");
}