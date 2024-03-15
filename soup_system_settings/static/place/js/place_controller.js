/* Полезные переменные */

let two_step_finish_patient = 1

let check_empty = null 

const additional = ['КТ', 'Рентген', 'Ортопантамограф', 'УЗИ', 'Лаборатория']

const  place_names = {'11':'Бокс 1', '12':'Бокс 2', '13':'Бокс 3','14':'Бокс 4','15':'Бокс 5', 
'21':'Смотровая 1','22':'Смотровая 2','23':'Смотровая 3', '24':'Смотровая 4', '25':'Смотровая 5'
}

const  place_names_revert = {'Бокс 1': '11', 'Бокс 2': '12', 'Бокс 3': '13','Бокс 4': '14', 'Бокс 5': '15', 
'Смотровая 1': '21','Смотровая 2': '22','Смотровая 3': '23', 'Смотровая 4': '24', 'Смотровая 5': '25' 
}

/* основные элементы */

const close_session_btn = document.getElementById('close_btn')

const close_session_div = document.getElementById('stop-agree')

const agree_close_btn = document.getElementById('agree-close-btn')

const not_agree_close_btn = document.getElementById('not-agree-close-btn')

const finish_patient_btn = document.getElementById('finish-patient-btn')

let noone_title = document.getElementById('noone')

let main_number = document.getElementById('main-number')

let next_doctors_form = document.getElementById('form')

let placeName = document.getElementById('place-name').textContent.trim()

let place_name_title = document.getElementById('place-name')

const departament = document.getElementById('departament-name').textContent.trim()

let doctor_fio =  document.getElementById('fio').textContent

let break_btn = document.getElementById('break-btn')

let return_btn = document.getElementById('return-btn')

let prompt_next_doctor = document.getElementById('prompt')

let not_return_input = document.getElementById('not_return')

check_p_title = document.getElementById('check-p')

/* Заполнение шаблона */

place_name_title.textContent = place_names[placeName]

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


function take_break(event) { 

  clearInterval(check_empty)
  check_empty = null 
  noone_title.classList.add('none-active')
  main_number.textContent = 'Идет перерыв'
  main_number.classList.remove('none-active')
  next_doctors_form.classList.add('none-active')
  finish_patient_btn.classList.add('none-active')
  break_btn.classList.add('none-active')
  return_btn.classList.remove('none-active')
  two_step_finish_patient = 1
  prompt_next_doctor.classList.add('none-active')

  ControllerSocket.send('{"break" : 1}')

}

function return_to_work(event) { 
  return_btn.classList.add('none-active')
  setTimeout(give_me_patient, 1500)
}


function finish_patient(event) { 

  console.log(two_step_finish_patient) 


  if (additional.includes(departament)) { 

    if (two_step_finish_patient === 1) {
      patient_form_submit()
      main_number.textContent = ''
      main_number.classList.add('none-active')
      break_btn.classList.remove('none-active')
      two_step_finish_patient++
      return 
    }

    if (two_step_finish_patient === 2) {
      break_btn.classList.add('none-active')
      finish_patient_btn.classList.add('none-active')
      prompt_next_doctor.classList.add('none-active')
      main_number.classList.remove('none-active') 
      two_step_finish_patient === 1
      setTimeout(give_me_patient, 1500)
      return 

    } 
  }


  if (two_step_finish_patient === 1) { 
    main_number.classList.add('none-active')
    next_doctors_form.classList.remove('none-active')
    two_step_finish_patient++
    return 
  }

  if (two_step_finish_patient === 2) {
    patient_form_submit()
    main_number.textContent = ''
    next_doctors_form.classList.add('none-active')
    break_btn.classList.remove('none-active')
    two_step_finish_patient++
    return 
  }

  if (two_step_finish_patient === 3) {
    two_step_finish_patient = 1
    setTimeout(give_me_patient, 1500)
    break_btn.classList.add('none-active')
    main_number.classList.remove('none-active')
    prompt_next_doctor.classList.add('none-active')
}

}

function patient_form_submit() { 
  let checked_departament = []
  const elements = form.elements;

  for (let i = 0; i < elements.length; i++) {
    const element = elements[i];
    if (element.checked) { 
      checked_departament.push(element.value)
    }
  }

  if (checked_departament.length === 0) { 
    checked_departament = 'nothing'
  }

  console.log(checked_departament)
  checked_departament = JSON.stringify(checked_departament)
  ControllerSocket.send(`{"end_patient": ${checked_departament}, "departament": "${departament}", "place": "${placeName}"}`)

  form.reset()
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

break_btn.onclick = take_break

return_btn.onclick = return_to_work



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
  setTimeout(() => finish_patient_btn.classList.remove('none-active'), 1999)
  };


ControllerSocket.onmessage = function(event) {

  let data = JSON.parse(event.data);

  if (data.break) { 
    return 
  }

  
  if (data.next_doctor) { 
    next_doctor = data.next_doctor
    prompt_next_doctor.textContent = `Следующее направление пациента - ${next_doctor}`
    prompt_next_doctor.classList.remove('none-active')
    return 
 }

  
  if (data['first_in'])  {
    not_return_input.classList.remove('none-active')
  }

  else { 
    not_return_input.classList.add('none-active')
  }

  let next_number = data.next_number

  console.log(next_number)

  if (!next_number && check_empty) { 
    return 
  }

  if (!next_number && !check_empty ) { 
    console.log(1000000)
    main_number.classList.add('none-active')
    noone_title.classList.remove('none-active')
    check_empty = setInterval(give_me_patient, 10000)
    finish_patient_btn.classList.add('none-active')
    break_btn.classList.remove('none-active') 
    return 
  }


  clearInterval(check_empty)
  check_empty = null 
  main_number.textContent = next_number
  noone_title.classList.add('none-active')
  main_number.classList.remove('none-active')
  noone_title.classList.add('none-active')
  finish_patient_btn.classList.remove('none-active')
  break_btn.classList.add('none-active') 

} 


window.addEventListener('beforeunload', function() {
  ControllerSocket.send('{"close" : 1}');
  ControllerSocket.close(1000);
});
  

