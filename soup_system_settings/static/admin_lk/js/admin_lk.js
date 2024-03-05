/* Основные элементы */ 

const close_remove_btn  = document.getElementById('close-remove')

const remove_div  = document.getElementById('remove-block')

const remove_btn = document.getElementById('remove-btn')


/* Функции евентов */

function close_remove(event) { 
    remove_div.classList.add('none-active')
}
 
function go_remove(event) { 
    
}


/* Присвоение евентов */

close_remove_btn.onclick = close_remove