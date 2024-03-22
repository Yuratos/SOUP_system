/* Переменные для работы  */ 

let to_delete = null 

const additional = JSON.parse(document.getElementById('additional_departaments').textContent);

const departaments_options = JSON.parse(document.getElementById('main_departaments').textContent);

console.log(additional)

console.log(departaments_options)


/* Основные элементы */ 

const close_remove_btn  = document.getElementById('close-remove')

const remove_div  = document.getElementById('remove-block')

const remove_btn = document.querySelectorAll('remove-btn-id')

let remove_btn_agree = document.getElementById('remove-btn-agree')

let remove_btn_disagree = document.getElementById('remove-btn-disagree')

let remove_text = document.getElementById('remove-text')

let ul_doctors = document.getElementById('person-list')

let search = document.getElementById('search')

let add_btn_click = document.getElementById('add-btn-click')

let add_form_block = document.getElementById('form-personal-div')

let close_add_form = document.getElementById('close-form add')

let select_form_choices = document.getElementById('depertamnet_choice')

let accept_new_personal_btn = document.getElementById('accept-new-personal-btn')

let doctor_form = document.getElementById('doctor-form')

let doctor_settings_click = document.getElementById('doctor-settings')

let place_settings_click = document.getElementById('place-settings')

let main_screen_title = document.getElementById('main-screen-title')

/* Функции-декораторы */

function debounce(foo) { 
  let tm = null 
  function wrapp(event) { 
      if (tm) { 
          clearTimeout(tm)
      }
      tm = setTimeout(foo, 1000, event)
  }
  return wrapp

}


/* Функции запросов */

function add_remove_doctor_api(method, fio, departament) { 

  let url = window.location.protocol + '//' + window.location.host + '/doctor/api/v1/add-remove-doctor'
  let json = JSON.stringify({ 
    method: method, 
    fio: fio, 
    departament: departament
  })
  console.log(json)
  const requestData = {
      method: 'PATCH', 
      headers: {
          'Content-Type': 'application/json' 
        },
           body: json
        };   

  fetch(url, requestData).catch(err => {console.log(err)})

}

function add_remove_place_api(method, place) { 

  let url = window.location.protocol + '//' + window.location.host + '/doctor/api/v1/add-remove-place'
  let json = JSON.stringify({ 
    method: method, 
    place: place, 
  })

  console.log(json)
  const requestData = {
      method: 'PATCH', 
      headers: {
          'Content-Type': 'application/json' 
        },
           body: json
        };   

  fetch(url, requestData).catch(err => {console.log(err)})

}



async function get_doctors(event) {
  let doctors = null 
  const currentUrl = window.location.protocol + '//' + window.location.host;
  const url = currentUrl + '/doctor/api/v1/doctor-list'

  if (!event || !event.target.value) {
      let response = await fetch(url)
      doctors = await response.json() 
} 
  
  else { 
      let params = {'search': event.target.value} 
      let queryParams = new URLSearchParams(params)
      const requestUrl = `${url}?${queryParams}`
      let response = await fetch(requestUrl)
      doctors = await response.json() } 

  ul_doctors.innerHTML = ""
  
  for (doctor of doctors.doctors) { 

    if (additional.includes(doctor))  {
      continue
    }

    let li_item = document.createElement('li')
    let li_h3_item = document.createElement('h3')
    let remove_btn = document.createElement('button')
    let img_cross = document.createElement('img') 
    img_cross.classList.add('icon-img')
    img_cross.src="/static/admin_lk/img/red-cross.svg"
    remove_btn.classList.add('remove-btn-id')
    remove_btn.appendChild(img_cross)
    remove_btn.onclick = go_remove
    li_h3_item.textContent = doctor
    li_item.appendChild(li_h3_item) 
    li_item.appendChild(remove_btn) 
    li_item.classList.add('person-card')
    ul_doctors.appendChild(li_item)
  }

}


async function get_places(event) {
  let places = null 
  const currentUrl = window.location.protocol + '//' + window.location.host;
  const url = currentUrl + '/doctor/api/v1/all-places'
  if (!event || !event.target.value) {
      let response = await fetch(url)
      places = await response.json() 
  } 

  else { 
      let params = {'search': event.target.value} 
      let queryParams = new URLSearchParams(params)
      const requestUrl = `${url}?${queryParams}`
      let response = await fetch(requestUrl)
      places = await response.json() } 

  ul_places.innerHTML = ""
  
  for (place of places.places) { 
      let li_item = document.createElement('li')
      let li_h3_item = document.createElement('h3')
      let remove_btn = document.createElement('button')
      let img_cross = document.createElement('img') 
      img_cross.classList.add('icon-img')
      img_cross.src="/static/admin_lk/img/red-cross.svg"
      remove_btn.classList.add('remove-btn-id')
      remove_btn.appendChild(img_cross)
      remove_btn.onclick = go_remove
      li_h3_item.textContent = place
      li_item.appendChild(li_h3_item) 
      li_item.appendChild(remove_btn) 
      li_item.classList.add('person-card')
      ul_doctors.appendChild(li_item)
  }
}


/* Функции евентов */

function close_remove(event) { 
    remove_div.classList.add('none-active')
}
 
function go_remove(event) { 
    to_delete = event.target.parentNode.previousElementSibling.textContent.split('-')
    console.log(to_delete)
    remove_text.textContent = `Вы уверены, что вы хотите удалить ${to_delete[0]}`
    remove_div.classList.remove('none-active')
}

function remove_doctor(event) { 
  add_remove_doctor_api('delete', to_delete[0].trim(), to_delete[1].trim())
  remove_div.classList.add('none-active')
  setTimeout(() => get_doctors(event = null), 1000)
}

function remove_place(event) { 
  add_remove_doctor_api('delete', to_delete[0])
  remove_div.classList.add('none-active')
  setTimeout(() => get_doctors(event = null), 1000)
}

function add_form(event) { 
  add_form_block.classList.remove('none-active')
  ul_doctors.classList.add('none-active')
}

function close_add_form_click(event) { 
  add_form_block.classList.add('none-active')
  ul_doctors.classList.remove('none-active')
}

function add_departament_to_select() { 
  for (option of departaments_options) {
    let opt = document.createElement('option') 
    opt.value = option
    opt.textContent = option
    select_form_choices.appendChild(opt) 
} 
}

function add_doctor(event) { 
  let i = 1 
  let fio = []
  let departament = ""
  const elements = doctor_form.elements;
  for (element of elements) { 
    element = element.value 
    if (!element) { 
      return
    }
    if (i != 4) { 
      fio.push(element)
    }
    if (i === 4) {
      departament = element 
    }
    
    i ++ 
  }

  fio = fio.join(" ")

  add_remove_doctor_api('add', fio, departament)

  add_form_block.classList.add('none-active')

  ul_doctors.classList.remove('none-active')

  setTimeout(() => get_doctors(event = null), 1000)

  doctor_form.reset()

}

function give_doctor_screen(event) { 
  main_screen_title.textContent = "Состав мед.работников, входящих в СУПП" 
  add_btn_click.firstElementChild.textContent = 'Добавить работника'
  remove_btn_agree.onclick = remove_doctor
  search.placeholder = 'Поиск по сотрудникам'
  search.oninput = debounce(get_doctors)
  get_doctors()
}

function give_doctor_screen(event) { 
  main_screen_title.textContent = "Кабинеты, зарегестрированные в системе СУПП" 
  remove_btn_agree.onclick = remove_place
  add_btn_click.firstElementChild.textContent = 'Добавить кабинет'
  search.placeholder = 'Поиск по кабинетам'
  search.oninput = debounce(get_places)
  get_places()
}


/* Присвоение евентов */

close_remove_btn.onclick = close_remove

remove_btn_disagree.onclick = close_remove

remove_btn_agree.onclick = remove_doctor

add_btn_click.onclick = add_form 

close_add_form.onclick = close_add_form_click

accept_new_personal_btn.onclick = add_doctor

get_doctors(event = null)

add_departament_to_select()