var hourly_container = document.getElementById("hourly_container");


function reload() {
    var city_name = document.getElementById("city_name").value;
    var address = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port  + window.location.pathname + "?city_name=" + city_name;
    location.href = address;
}

function display_one_hour_data(hourly_data){
    background_src = "/static/images/" + hourly_data[0].icon_name + ".jpg";
    document.getElementById("main_image").src = background_src;

    for(let i = 0; i < hourly_data.length; i++) {
        let obj = hourly_data[i];

        const node_time = document.createTextNode(obj.hour + ":00");
        const time_mark = document.createElement("p");
        time_mark.classList.add("time_mark");
        time_mark.appendChild(node_time);

        const node_temp = document.createTextNode(Math.round(obj.temp));
        const celsius_sign = document.createTextNode("℃");
        const celsius = document.createElement("span");
        celsius.classList.add("small");
        celsius.appendChild(celsius_sign);

        const temperature = document.createElement("p");
        temperature.appendChild(node_temp);
        temperature.appendChild(celsius);

        const icon = document.createElement("img");
        icon.src = "/static/icons/" + obj.icon_name + ".png";
        const icon_wrapper = document.createElement("p");
        icon_wrapper.classList.add("small");
        icon_wrapper.appendChild(icon);

        const forcast_div = document.createElement("div");
        forcast_div.classList.add("forcast");
        forcast_div.appendChild(time_mark);
        forcast_div.appendChild(temperature);
        forcast_div.appendChild(icon_wrapper);

        hourly_container.appendChild(forcast_div);
    }
}

function set_background_size(){
    /* Make sure image is square to make this work */
    var main_image = document.getElementById("main_image");

    const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

    var img_size = vw;
    if(vw < vh){
        img_size = vh;
    }

    main_image.style.height = img_size + "px";
    main_image.style.width = img_size + "px";
}

function display_multiple_hour_data(hourly_data, hours){
    var interval = 0;
    var start_hour;
    var end_hour;
    var start_temp;
    var end_temp;
    var max_temp;
    var icon_name;
    var precipitation;
    var weathercode;

    for(let i = 0; i < hourly_data.length; i++){
        let obj = hourly_data[i];
        precipitation = obj.prec;
        weathercode = obj.wc;

        if(interval == 0){
            start_hour = obj.hour;
            icon_name = obj.icon_name;
            start_temp = obj.temp;
            max_temp = obj.temp;
            min_temp = obj.temp;
        }else{
            if(max_temp < obj.temp){
                max_temp = obj.temp;
            }
            if(min_temp > obj.temp){
                min_temp = obj.temp;
            }

            if((interval >= hours) || (obj.prec == 0 && precipitation != 0) || (obj.prec != 0 && precipitation == 0)){
                end_hour = obj.hour;
                end_temp = obj.temp;

                const node_time = document.createTextNode(start_hour + ":00 - " + end_hour + ":00");
                const time_mark = document.createElement("p");
                time_mark.classList.add("time_mark");
                time_mark.appendChild(node_time);

                const temperature = document.createElement("p");
                if((max_temp - min_temp) < 2){
                    const node_temp = document.createTextNode(Math.round((start_temp + end_temp)/2));
                    const celsius_sign = document.createTextNode("℃");
                    const celsius = document.createElement("span");
                    celsius.classList.add("small");
                    celsius.appendChild(celsius_sign);

                    temperature.appendChild(node_temp);
                    temperature.appendChild(celsius);
                }else{
                    const node_temp_1 = document.createTextNode(Math.round(start_temp));
                    const celsius_sign_1 = document.createTextNode("℃");
                    const celsius_1 = document.createElement("span");
                    celsius_1.classList.add("small");
                    celsius_1.appendChild(celsius_sign_1);
                    const node_temp_2 = document.createTextNode(" .. " + Math.round(end_temp));
                    const celsius_sign_2 = document.createTextNode("℃");
                    const celsius_2 = document.createElement("span");
                    celsius_2.classList.add("small");
                    celsius_2.appendChild(celsius_sign_2);
                    temperature.appendChild(node_temp_1);
                    temperature.appendChild(celsius_1);
                    temperature.appendChild(node_temp_2);
                    temperature.appendChild(celsius_2);
                }

                const icon = document.createElement("img");
                icon.src = "/static/icons/" + icon_name + ".png";
                const icon_wrapper = document.createElement("p");
                icon_wrapper.classList.add("small");
                icon_wrapper.appendChild(icon);

                const forcast_div = document.createElement("div");
                forcast_div.classList.add("forcast");
                forcast_div.appendChild(time_mark);
                forcast_div.appendChild(temperature);
                forcast_div.appendChild(icon_wrapper);

                hourly_container.appendChild(forcast_div);

                start_hour = obj.hour;
                icon_name = obj.icon_name;
                start_temp = obj.temp;
                max_temp = obj.temp;
                interval = 0;
            }else{
                if(weathercode < obj.wc){
                    icon_name = obj.icon_name;
                    weathercode = obj.wc;
                }
            }
        }
        interval++;
    }
}

function distribute_forcasts(){

    var forecast_divs = hourly_container.getElementsByTagName('div');
    var num_of_children = forecast_divs.length - 1;
    var total_width = window.innerWidth;
    var min_width = Math.round(total_width/(num_of_children + 1)) - 5;
    var produced_width = 0;

    for(var i=0; i<num_of_children; i++) {
        forecast_divs[i].style.minWidth = min_width + "px";
    }
}

function populate_hourly_forcast(){
    var data = document.getElementById("hourly_data").value.replaceAll("'", '"');
    try{
        const hourly_data = JSON.parse(data);

        display_one_hour_data(hourly_data);
        if(hourly_container.clientWidth < hourly_container.scrollWidth){
            console.log("Overflow");

            for(let i = 2; i < 9; i++){
                hourly_container.innerHTML = "";
                display_multiple_hour_data(hourly_data, i);
                if(hourly_container.scrollWidth <= hourly_container.clientWidth){
                    console.log("Overflow " + i);
                    break;
                }else{
                    console.log("Overflow " + i);
                }
            }
        }

    }catch(error){
        console.error(error);
    }
}

window.onload = function() {
    populate_hourly_forcast();
    distribute_forcasts();
    set_background_size();
    // Refresh every half an hour
    setTimeout(reload, 1800000);
}