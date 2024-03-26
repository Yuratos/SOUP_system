/* основные элементы */

const placeName = JSON.parse(document.getElementById('place_number').textContent);

let main_number = document.getElementById('main_number');

let not_active_title = document.getElementById('not-active');

let pause_title = document.getElementById('pause');

let doctor_name  = document.getElementById('doctor_name');

let place_name_title = document.getElementById('place-name')


let checker = 0


/* Веб-сокет */

const placeSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/place/'
    + placeName
    + '/'
);


/* Заполнение шаблона */

place_name_title.textContent = `${placeName}`


/* Действия с веб-сокетом  */

placeSocket.onmessage = function(event) {
    let data = JSON.parse(event.data);

    console.log(data)

    if (data.next_doctor) { 
        return
    }

    // Врач зарегался на месте
    if (data.fio && data.fio !== "Идут сопутствующие процедуры") {
        let place_doctor_fio = data.fio
        doctor_name.textContent = `Принимающий врач: ${place_doctor_fio}`
        not_active_title.classList.add('none-active') 
        pause_title.classList.add('none-active') 
    }

    // Врач ушёл - кабинет закрывается
    if (data.close) { 
        main_number.textContent = '' 
        not_active_title.classList.remove('none-active') 
        doctor_name.textContent = ''
        return
    }

    // Врач взял перерыв
    if (data.break) { 
        console.log('break')
        pause_title.classList.remove('none-active') 
        main_number.classList.add('none-active') 
        not_active_title.classList.add('none-active')
        return  
    }

    if (data.fio == "Идут сопутствующие процедуры") { 
        doctor_name.textContent = ''
        not_active_title.classList.add('none-active') 
    }

    console.log(data.fio)

    let place_main_number = data.next_number
    console.log(place_main_number)
    main_number.textContent = place_main_number 
    main_number.classList.remove('none-active') 
    pause_title.classList.add('none-active') 
    if (place_main_number === 0) { 
        console.log("FDFSF")
        main_number.textContent = ''
    }
    

};


placeSocket.onclose = function(event) {
    not_active_title.hidden = false
};


window.addEventListener('beforeunload', function() {
    ControllerSocket.close(1001);
  });
    