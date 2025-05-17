document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-rating-item');
    const ratingInput = document.getElementById('rating-value');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const selectedRating = parseInt(this.getAttribute('data-rating'));
            const currentRating = parseInt(ratingInput.value || '0');

            // Если пользователь кликает на ту же звезду — сбрасываем рейтинг
            const newRating = selectedRating === currentRating ? 0 : selectedRating;
            ratingInput.value = newRating;

            stars.forEach((s, index) => {
                if (index < newRating) {
                    s.classList.remove('bi-star');
                    s.classList.add('bi-star-fill');
                } else {
                    s.classList.remove('bi-star-fill');
                    s.classList.add('bi-star');
                }
            });
        });
    });

    // Установка звёзд при загрузке
    const initialRating = parseInt(ratingInput.value || '0');
    stars.forEach((s, index) => {
        if (index < initialRating) {
            s.classList.remove('bi-star');
            s.classList.add('bi-star-fill');
        }
    });
});