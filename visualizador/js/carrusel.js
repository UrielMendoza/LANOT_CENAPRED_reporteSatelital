// document.addEventListener('DOMContentLoaded', () => {
//     const elementosCarousel = document.querySelectorAll('.carousel');

//     M.Carousel.init(elementosCarousel, {
//         duration: 100,
//         dist: -60,
//         numVisible: 6,
//         shift: 6,
//         indicators: true,

//     })
// });
$(document).ready(carousel);

function carousel(){
    $('.carousel').carousel({
        interval: 5000
      })
}
