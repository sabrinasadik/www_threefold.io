'use strict';

var xhr = new XMLHttpRequest();

var price = document.getElementById('price');
var volume = document.getElementById('volume');
var stats = document.getElementById('stats');
var capitalization = document.getElementById('capitalization');
var capSum, volSum, res, result;

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
xhr.open('GET', 'https://radar.threefold.me/api/v1', true);

xhr.onload = function () {

    // Begin accessing JSON data here
    var data = JSON.parse(this.response);

    if (xhr.status >= 200 && xhr.status < 400) {

        // price.innerHTML = data.data.currency.tftPrice.pairs.TFT_USD.price + ' USD/TFT';
        // stats.innerHTML = '$' + data.data.currency.tftPrice.pairs.TFT_USD.price;
        capSum = Math.round((data.data.totalSupply / 1000000000) * data.data.currency.tftPrice.weightedAveragePrice);
        res = capSum.toString();
        capitalization.innerHTML = '$' + res.slice(0, 2) + ' million';
        volSum = Math.round(data.data.currency.tftPrice.dailyTradingVolume);
        result = numberWithCommas(volSum);
        volume.innerHTML = '$' + result;
    } else {
        console.log('error');
    }
}
xhr.send();