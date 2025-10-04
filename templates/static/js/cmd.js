$(document).ready(function () {
    $('#logout-link').click(function (event) {
        event.preventDefault();
        var logoutUrl = $(this).data('logout-url');
        $.post(logoutUrl, function () {
            window.location.href = '/';
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const thumbs = document.querySelectorAll('.home-carousel-thumb-semprevivas');
    const slides = document.querySelectorAll('.home-carousel-slide-semprevivas');

    thumbs.forEach(thumb => {
        thumb.addEventListener('click', function() {
            const index = this.getAttribute('data-index');

            thumbs.forEach(t => t.classList.remove('active'));
            slides.forEach(s => s.classList.remove('active'));

            this.classList.add('active');
            slides[index].classList.add('active');
        });
    });
});
