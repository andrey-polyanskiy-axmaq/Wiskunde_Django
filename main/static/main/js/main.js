const menuBtn = document.querySelector('.menu__btn');
const menuClose = document.querySelector('.menu__close');
const menuList = document.querySelector('.menu');

menuList.classList.remove('menu__list--open')

menuBtn.addEventListener('click', () => {
    menuList.classList.add('menu__list--open')
});

menuClose.addEventListener('click', () => {
    menuList.classList.remove('menu__list--open')
});

let coll = document.getElementsByClassName('collapsible');
for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener('click', function () {
        this.classList.toggle('active');
        let content = this.nextElementSibling;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + 'px';
        }
    })
}

document.addEventListener('DOMContentLoaded', function() {
    var button = document.querySelector('.top_button-sign-up');
    var targetSection = document.querySelector('.index__course-description');

    button.addEventListener('click', function() {
        targetSection.scrollIntoView({ behavior: 'smooth' });
    });
});

