/* Переменные для работы  */ 

let to_delete = null 

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

let add_form_block = document.getElementById('add-personal-form-block')

let close_add_form = document.getElementById('close-form add')


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

function add_form(event) { 
  add_form_block.classList.remove('none-active')
}

function close_add_form_click(event) { 
  add_form_block.classList.add('none-active')
}


/* Присвоение евентов */

close_remove_btn.onclick = close_remove

remove_btn_disagree.onclick = close_remove

remove_btn_agree.onclick = remove_doctor

search.oninput = debounce(get_doctors)

add_btn_click.onclick = add_form 

close_add_form.onclick = close_add_form_click



get_doctors(event = null)