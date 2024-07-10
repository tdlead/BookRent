console.log('hello world from base dir')
const goBack = document.getElementById('go-back-btn')

goBack?.addEventListener('click', () => history.back() )