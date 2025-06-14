/* JavaScript для работы с формой отзывов */
document.addEventListener("DOMContentLoaded", function () {
    // Инициализация обработчика для звездочек рейтинга
    initRatingStats();
    // Инициализация AJAX для загрузки данных о мастере
    initMasterInfoLoader();
    // Инициализация валидации формы
    initFormValidation();
});

/* Инициализация обработчика для звездочек рейтинга */
function initRatingStats() {
    const stars = document.querySelectorAll('.star-rating-item');
    const ratingInput = document.getElementById('rating-value');
    
    // ✅ Общая функция для обновления звездочек
    function setStarsState(rating) {
        stars.forEach((star) => {
            const starValue = star.getAttribute("data-rating");
            // Используем toggle для более элегантного переключения классов
            star.classList.toggle("bi-star-fill", starValue <= rating);
            star.classList.toggle("bi-star", starValue > rating);
        });
    }
    
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.getAttribute("data-rating");
            ratingInput.value = rating;
            // Используем общую функцию
            setStarsState(rating);
        });
               
        // Добавляем эффект при наведении
        star.addEventListener("mouseover", function () {
            const hoverRating = this.getAttribute("data-rating");
            // Используем общую функцию
            setStarsState(hoverRating);
        });
        
        // Возвращаем выбранное состояние при уходе курсора
        star.addEventListener("mouseout", function () {
            const currentRating = ratingInput.value || 0;
            // Используем общую функцию
            setStarsState(currentRating);
        });
    });
}

/* Отображение информации о мастере */
function displayMasterInfo(master, masterInfoDiv) {
    if (!masterInfoDiv) return;
    
    // Очищаем предыдущую информацию
    masterInfoDiv.innerHTML = "";
    
    // Создаем карточку с информацией о мастере
    const card = document.createElement("div");
    card.className = "card mt-3";
    
    // Добавляем фото мастера, если оно есть
    if (master.photo) {
        const img = document.createElement("img");
        img.src = master.photo;
        img.className = "rounded-circle";
        img.alt = master.name;
        img.style.width = "100px";
        img.style.height = "100px";
        img.style.objectFit = "cover";
        card.appendChild(img);
    }
    
    // Добавляем информацию о мастере
    const cardBody = document.createElement("div");
    cardBody.className = "card-body";
    
    const title = document.createElement("h5");
    title.className = "card-title";
    title.textContent = master.name;
    
    const experience = document.createElement("p");
    experience.className = "card-text";
    experience.textContent = `Опыт работы: ${master.experience} лет`;
    
    cardBody.appendChild(title);
    cardBody.appendChild(experience);
    
    // Добавляем список услуг мастера
    if (master.services && master.services.length > 0) {
        const servicesTitle = document.createElement("h6");
        servicesTitle.className = "card-subtitle mb-2 mt-3";
        servicesTitle.textContent = "Предоставляемые услуги:";
        cardBody.appendChild(servicesTitle);
        
        const servicesList = document.createElement("ul");
        servicesList.className = "list-group list-group-flush";
        
        master.services.forEach((service) => {
            const listItem = document.createElement("li");
            listItem.className = "list-group-item d-flex justify-content-between align-items-center";
            listItem.textContent = service.name;
            
            const badge = document.createElement("span");
            badge.className = "badge bg-primary rounded-pill";
            badge.textContent = `${service.price} руб.`;
            
            listItem.appendChild(badge);
            servicesList.appendChild(listItem);
        });
        
        cardBody.appendChild(servicesList);
    }
    
    card.appendChild(cardBody);
    masterInfoDiv.appendChild(card);
}

/* Инициализация AJAX для загрузки данных о мастере */
function initMasterInfoLoader() {
    const masterSelect = document.getElementById('master');
    const masterInfoDiv = document.getElementById('master-info-container');
    
    if (masterSelect && masterInfoDiv) {
        masterSelect.addEventListener("change", function () {
            const masterId = this.value;
            if (masterId) {
                fetch(`/barbershop/api/master-info/?master_id=${masterId}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                })
                .then(response => response.json())
                .then((data) => {
                    if (data.success) {
                        displayMasterInfo(data.master, masterInfoDiv);
                    } else {
                        console.error("Ошибка:", data.error);
                        masterInfoDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    }
                })
                .catch((error) => {
                    console.error("Ошибка загрузки данных:", error);
                    masterInfoDiv.innerHTML = '<div class="alert alert-danger">Ошибка загрузки данных о мастере</div>';
                });
            } else {
                masterInfoDiv.innerHTML = '';
            }
        });
        
        // Если мастер уже выбран при загрузке страницы, загружаем информацию о нем
        if (masterSelect.value) {
            masterSelect.dispatchEvent(new Event("change"));
        }
    }
}

/* Инициализация клиентской валидации формы */
function initFormValidation() {
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            if (!validateReviewForm()) {
                event.preventDefault();
            }
        });
    }
    
    /* Основная функция валидации формы */
    function validateReviewForm() {
        let isValid = true;
        
        // Валидация имени клиента
        const clientNameInput = document.getElementById("id_client_name");
        if (clientNameInput && clientNameInput.value.trim() === "") {
            isValid = false;
            showError(clientNameInput, "Пожалуйста, укажите ваше имя");
        } else if (clientNameInput) {
            clearError(clientNameInput);
        }
        
        // Валидация текста отзыва
        const textInput = document.getElementById("id_text");
        if (textInput && textInput.value.trim() === "") {
            isValid = false;
            showError(textInput, "Пожалуйста, напишите текст отзыва");
        } else if (textInput && textInput.value.trim().length < 10) {
            isValid = false;
            showError(
                textInput,
                "Текст отзыва должен содержать не менее 10 символов"
            );
        } else if (textInput) {
            clearError(textInput);
        }
        
        // Валидация рейтинга
        const ratingInput = document.getElementById("id_rating");
        if (ratingInput && (!ratingInput.value || parseInt(ratingInput.value) < 1)) {
            isValid = false;
            // Показываем ошибку возле звездочек
            const ratingStars = document.querySelector(".rating-stars");
            if (ratingStars) {
                showErrorNear(ratingStars, "Пожалуйста, выберите оценку");
            }
        } else {
            // Убираем сообщение об ошибке возле звездочек
            const ratingStars = document.querySelector(".rating-stars");
            if (ratingStars) {
                clearErrorNear(ratingStars);
            }
        }
        
        // Валидация выбора мастера
        const masterSelect = document.getElementById("id_master");
        if (masterSelect && (!masterSelect.value || masterSelect.value === "")) {
            isValid = false;
            showError(masterSelect, "Пожалуйста, выберите мастера");
        } else if (masterSelect) {
            clearError(masterSelect);
        }
        
        return isValid;
    }
    
    /* Показ сообщения об ошибке */
    function showError(element, message) {
        // Удаляем предыдущую ошибку
        clearError(element);
        // Добавляем класс is-invalid
        element.classList.add("is-invalid");
        // Создаем элемент для сообщения об ошибке
        const errorDiv = document.createElement("div");
        errorDiv.className = "invalid-feedback";
        errorDiv.textContent = message;
        // Добавляем сообщение после элемента
        element.parentNode.appendChild(errorDiv);
    }
    
    /* Показ сообщения об ошибке рядом с элементом (не для input) */
    function showErrorNear(element, message) {
        // Удаляем предыдущую ошибку
        clearErrorNear(element);
        // Создаем элемент для сообщения об ошибке
        const errorDiv = document.createElement("div");
        errorDiv.className = "text-danger mt-2 rating-error";
        errorDiv.textContent = message;
        // Добавляем сообщение после элемента
        element.parentNode.appendChild(errorDiv);
    }
    
    /* Очистка сообщения об ошибке для input */
    function clearError(element) {
        // Убираем класс is-invalid
        element.classList.remove("is-invalid");
        // Удаляем сообщение об ошибке, если оно есть
        const errorMessage = element.parentNode.querySelector(".invalid-feedback");
        if (errorMessage) {
            errorMessage.remove();
        }
    }
    
    /* Очистка сообщения об ошибке рядом с элементом */
    function clearErrorNear(element) {
        // Удаляем сообщение об ошибке, если оно есть
        const errorMessage = element.parentNode.querySelector(".rating-error");
        if (errorMessage) {
            errorMessage.remove();
        }
    }
}