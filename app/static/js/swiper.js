import Swiper from 'swiper/bundle';
import { Pagination } from 'swiper/modules';
import 'swiper/css/bundle';
import 'swiper/css/pagination';
import 'swiper/css/effect-cards';
import "./app/static/css/input.css";


const swiper = new Swiper('.proofSlides', {
    effect: "cube",
    cubeEffect : {
        slideShadows: false,
        shadow: false,
        shadowOffset: 20,
        shadowScale: 0.94,
    },
    loop: true,
    autoplay : {
        delay: 3000,
        duration : 500
    },
    grabCursor: true,
    modules: [Pagination],
    centeredSlides: true,
    pagination: {
        el: '.swiper-pagination',
    }
});
