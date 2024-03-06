/* основные элементы */

const placeName = JSON.parse(document.getElementById('place_number').textContent);

let main_number = document.getElementById('main_number');

let not_active_title = document.getElementById('not-active');

let doctor_name  = document.getElementById('doctor_name');

let checker = 0


/* Веб-сокет */

const placeSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/place/'
    + placeName
    + '/'
);


/* Действия с веб-сокетом  */

placeSocket.onmessage = function(event) {
    let data = JSON.parse(event.data);

    console.log(data)

    if (data.close) { 
        main_number.textContent = '' 
        not_active_title.classList.remove('none-active') 
        doctor_name.textContent = ''
        return
    }

    console.log(data.fio)

    if (data.fio == "Идут сопутствующие процедуры") { 
        doctor_name.textContent = `${data.departament}`
        not_active_title.classList.add('none-active') 
    }


    if (data.fio && data.fio !== "Идут сопутствующие процедуры") {
        let place_doctor_fio = data.fio
        doctor_name.textContent = `Принимающий врач: ${place_doctor_fio}`
        not_active_title.classList.add('none-active') 
    }

    let place_main_number = data.next_number
    console.log(place_main_number)
    main_number.textContent = place_main_number 

    

};


placeSocket.onclose = function(event) {
    not_active_title.hidden = false
};


window.addEventListener('beforeunload', function() {
    ControllerSocket.close(1001);
  });
    