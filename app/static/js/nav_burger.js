// const mainMenu = document.querySelector('.mainMenu');
const closeMenu = document.querySelector('.nav_menu_close');
const openMenu = document.querySelector('.nav_menu_open');




openMenu.addEventListener('click',show);
closeMenu.addEventListener('click',close);

function show(){
    navbar.style.display = 'flex';
    navbar.style.top = '0';
}
function close() {
    navbar.style.top = '-100%';
}