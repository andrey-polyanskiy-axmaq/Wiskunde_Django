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

document.addEventListener('DOMContentLoaded', function () {
    var signUpButton = document.querySelector('.description_button-sign-up');
    signUpButton.addEventListener('click', function() {
        window.location.href = 'https://vk.com/im?media=&sel=-224857793';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var signUpButton = document.querySelector('.top_button-sign-up');
    signUpButton.addEventListener('click', function() {
        window.location.href = 'https://vk.com/im?media=&sel=-224857793';
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     const scrollContainer = document.querySelector('.features_items-grid');
//
//     scrollContainer.addEventListener('scroll', function() {
//         var maxScrollLeft = scrollContainer.scrollWidth - scrollContainer.clientWidth;
//         if (scrollContainer.scrollLeft >= maxScrollLeft - 10) {
//             scrollContainer.scrollLeft = 0;
//         }
//         else if (scrollContainer.scrollLeft <= 10) {
//              scrollContainer.scrollLeft = maxScrollLeft;
//         }
//     });
// });

