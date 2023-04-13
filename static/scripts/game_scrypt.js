'use strict'

var showed_1 = false;

function show_1() {
    showed_1 = !showed_1;
    var image_1_1 = document.getElementById("player1_card_1");
    var image_1_2 = document.getElementById("player1_card_2");
    if (showed_1 == true) {
        image_1_1.src = '/static/img/cards/default0.png';
        image_1_2.src = '/static/img/cards/default0.png';
    } else {
        image_1_1.src = card1;
        image_1_2.src = card2;
    }
}

