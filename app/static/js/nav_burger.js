const toggleButton = document.getElementsByClassName('toggle-button')[0]
const navbarLinks = document.getElementsByClassName('nav-links')[0]
const navbarLinks2 = document.getElementsByClassName('nav-links')[1]
toggleButton.addEventListener('click', () => {
  navbarLinks.classList.toggle('active')
  navbarLinks2.classList.toggle('active')
})