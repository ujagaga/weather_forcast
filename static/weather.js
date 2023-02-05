function reload() {
    var city_name = document.getElementById("city_name").value;
    var address = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port  + window.location.pathname + "?city_name=" + city_name;
    location.href = address;
}

window.onload = function() {
    // Refresh every half an hour
    setTimeout(reload, 1800000);
}