/* Полезные переменные */

let two_step_finish_patient = 1

let check_empty = null 

/* основные элементы */

const close_session_btn = document.getElementById('close_btn')

const close_session_div = document.getElementById('stop-agree')

const agree_close_btn = document.getElementById('agree-close-btn')

const not_agree_close_btn = document.getElementById('not-agree-close-btn')

const finish_patient_btn = document.getElementById('finish-patient-btn')

let noone_title = document.getElementById('noone')

let main_number = document.getElementById('main-number')

let next_doctors_form = document.getElementById('form')

const placeName = document.getElementById('place-name').textContent.replaceAll(' ', '')

const departament = document.getElementById('departament-name').textContent.replaceAll(' ', '')

let doctor_fio =  document.getElementById('fio').textContent



/* Функции для евентов */

function close_table_session(event) { 
  close_session_div.classList.remove('none-active')
}

function not_agree_with_close(event) { 
  close_session_div.classList.add('none-active')
}
 
function agree_with_close(event) { 
  const currentUrl = window.location.protocol + '//' + window.location.host;
  window.location.href = currentUrl + '/doctor/doctor-page/'
}


function finish_patient(event) { 
  console.log(two_step_finish_patient)
  if (two_step_finish_patient === 1) { 
    console.log(1)
    main_number.classList.add('none-active')
    next_doctors_form.classList.remove('none-active')
    two_step_finish_patient++
    return 
  }

  if (two_step_finish_patient === 2) {
    patient_form_submit()
    main_number.textContent = ''
    main_number.classList.remove('none-active')
    finish_patient_btn.classList.add('none-active')
    next_doctors_form.classList.add('none-active')
    two_step_finish_patient = 1

    setTimeout(give_me_patient, 1500)
  }
}


function patient_form_submit() { 
  let checked_departament = []
  const elements = form.elements;

  for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    if (element.checked) { 
      checked_departament.push(element.value)
      element.removeAttribute('checked')
    }
  }

  checked_departament = JSON.stringify(checked_departament)
  ControllerSocket.send(`{"end_patient": ${checked_departament}, "departament": "${departament}", "place": "${placeName}"}`)

}


/* Функции для вебсокета */

function give_me_patient(event) { 
  ControllerSocket.send(`{"departament" : "${departament}", "place": "${placeName}"}`)
}


/* Присвоение евентов */

close_session_btn.onclick = close_table_session

agree_close_btn.onclick = agree_with_close

not_agree_close_btn.onclick = not_agree_with_close

finish_patient_btn.onclick = finish_patient





/* Веб-сокет */

const ControllerSocket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/place/'
  + placeName
  + '/?open', 
  
);

/* Действия с веб-сокетом  */

ControllerSocket.onopen = function(event) {
  console.log(doctor_fio)
  setTimeout(() => ControllerSocket.send(`{"departament" : "${departament}", "place": "${placeName}", "fio": "${doctor_fio}"}`), 2000)
  setTimeout(() => finish_patient_btn.classList.remove('none-active'), 1900)
  };


ControllerSocket.onmessage = function(event) {

  let data = JSON.parse(event.data);

  let next_number = data.next_number

  console.log(next_number)

  if (!next_number && check_empty) { 
    return 
  }

  if (!next_number && !check_empty ) { 
    main_number.classList.add('none-active')
    noone_title.classList.remove('none-active')
    check_empty = setInterval(give_me_patient, 10000)
    finish_patient_btn.classList.add('none-active')
    return 
  }


  clearInterval(check_empty)
  check_empty = null 
  noone_title.classList.add('none-active')
  main_number.classList.remove('none-active')
  noone_title.classList.add('none-active')
  finish_patient_btn.classList.remove('none-active')
  main_number.textContent = next_number

} 


window.addEventListener('beforeunload', function() {
  ControllerSocket.send('{"close" : 1}');
  ControllerSocket.close(1000);
});
  


