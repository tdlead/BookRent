const formModal= document.getElementById('form-modal')
console.log(formModal)
const openModalBtn = document.getElementById('open-modal-btn')
console.log(openModalBtn)
openModalBtn.addEventListener('click', ()=> {
    formModal.classList.remove('hidden')
})

const cancelBtn = document.getElementById('cancel-btn')

cancelBtn.addEventListener('click', ()=> {
    formModal.classList.add('hidden')
})

const backdrop =  document.getElementById('backdrop')

//add event on clicking outside backdrop
formModal.addEventListener('click', (e)=> {
    console.log(e.target)
    if(e.target !== backdrop) return;
    formModal.classList.add('hidden')
})