const copyBtnBox = document.getElementById('copy-btn-box')
const bookIdCopy = document.getElementById('book-id-box')

copyBtnBox.addEventListener('click', ()=>{
    const bookId = bookIdCopy.textContent;

    navigator.clipboard.writeText(bookId).then(() => {
        copyBtnBox.innerHTML="<p>copied!</p>"
    } )
})