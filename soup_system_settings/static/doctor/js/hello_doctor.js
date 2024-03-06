/* Глобальные переменные для передачи в Контроллер */

let main_doctor = null 

let main_place = null

const additional_places = ['МРТ', 'Сдача крови', 'Сдача мочи', 'СКТ']



/* основные элементы'*/


let firstContainerStep = document.getElementById('first-step')

let secondContainerStep = document.getElementById('second-step')

let thirdContainerStep = document.getElementById('third-step')

let ul_doctors = document.getElementById('doctor-list')

let ul_places =  document.getElementById('places-list')

let inp_search_doctors = document.getElementById('inp-search-doctors')

let hello_text_step_third = document.querySelector('.hello-text')

let = inp_search_places = document.getElementById('inp-search-places')

let sorry_text_second = document.getElementById('sorry-block-second')

let sorry_text_third = document.getElementById('sorry-block-third')



/* конпки */
let startBtn = document.getElementById('start-btn')

let second_step_back_btn = document.getElementById('btn-back-step-second')

let third_step_back_btn = document.getElementById('btn-back-step-third')


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

    if (doctors.doctors.length === 0) { 
        sorry_text_second.classList.remove('none-active')
        return
    }

    
    sorry_text_second.classList.add('none-active')

    console.log(doctors.doctors)

    doctors.doctors.push(...additional_places)

    for (doctor of doctors.doctors) { 
        let btn = document.createElement('button')
        let li_item = document.createElement('li')
        let li_h3_item = document.createElement('h3')
        li_h3_item.textContent = doctor
        li_item.appendChild(li_h3_item) 
        li_item.classList.add('doctor-item')
        li_item.onclick = choose_doctors
        btn.appendChild(li_item)
        ul_doctors.appendChild(btn)
    }


}


async function get_places(event) {
    let places = null 
    const currentUrl = window.location.protocol + '//' + window.location.host;
    const url = currentUrl + '/doctor/api/v1/free-places'
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

    if (!places.places) {
        sorry_text_third.classList.remove('none-active')
        return 
        }

    ul_places.innerHTML = ""

    if (places.places .length === 0) { 
        sorry_text_third.classList.remove('none-active')
        return
    }

    sorry_text_third.classList.add('none-active')

    for (place of places.places) { 
        let btn = document.createElement('button')
        let li_item = document.createElement('li')
        let li_h3_item = document.createElement('h3')
        li_h3_item.textContent = place
        li_item.appendChild(li_h3_item) 
        li_item.classList.add('doctor-item')
        li_item.onclick = choose_places
        btn.appendChild(li_item)
        ul_places.appendChild(btn)
    }

}


/* Функции для евентов */

function starBtnEvent(event) { 
    firstContainerStep.classList.add('none-active')
    get_doctors().catch(err => {console.log(err)})
    secondContainerStep.classList.remove('none-active')
    }

function choose_doctors(event) { 
    main_doctor = event.target.textContent
    main_doctor_name_list = main_doctor.split(' ')

    if (main_doctor_name_list.length <= 3) { 

        hello_text_step_third.textContent = `Добрый день. Выбрано: ${main_doctor_name_list.join(' ')}`

    } else {

        hello_text_step_third.textContent = `Добрый день, ${main_doctor_name_list[0]} ${main_doctor_name_list[1]}` 
    }

    get_places(event=null).catch(err => {console.log(err)})
    secondContainerStep.classList.add('none-active')
    thirdContainerStep.classList.remove('none-active')
}


function choose_places(event) { 
    main_place = event.target.textContent
    let url = 'http://' + window.location.host + `/place/place-controller/${main_place}/${main_doctor}`
    window.location.href = url

}

function back_btn_second(event) {
    inp_search_doctors.value = ''
    secondContainerStep.classList.add('none-active') 
    firstContainerStep.classList.remove('none-active')
}

function back_btn_third(event) {
    inp_search_places.value = ''
    thirdContainerStep.classList.add('none-active') 
    secondContainerStep.classList.remove('none-active')
}


/* Функция-старт  */ 

function first_srep() { 
    startBtn.addEventListener('click', starBtnEvent)
    inp_search_doctors.oninput =  debounce(get_doctors)
    second_step_back_btn.onclick = back_btn_second
    third_step_back_btn.onclick = back_btn_third
    inp_search_places.oninput =  debounce(get_places)

}


/* Начало загрузки страницы */
first_srep()
get_doctors(event = null).catch(err => {console.log(err)})






