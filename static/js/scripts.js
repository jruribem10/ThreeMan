/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
window.addEventListener('scroll', function() {
    var sidebar = document.querySelector('.sidebar');
    if (window.scrollY > 100) {
        sidebar.classList.add('is-scrolling');
    } else {
        sidebar.classList.remove('is-scrolling');
    }
});
