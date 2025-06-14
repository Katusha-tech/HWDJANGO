// Модульная структура для order_form.js
// Все функции объявлены отдельно
// Улучшенная версия order_form.js с отладкой
// Защита от двойной инициализации
// Защита от двойной инициализации
// Защита от двойной инициализации
if (window._orderFormInitialized) {
  console.warn("order_form.js уже инициализирован!");
} else {
  window._orderFormInitialized = true;

  // Селекторы элементов
  const SELECTORS = {
    MASTER_SELECT: '#master, select[name="master"]',
    SERVICES_SELECT: '#services, select[name="services"]',
    ORDER_FORM_DATA: '#order-form-data',
    CSRF_TOKEN: '[name=csrfmiddlewaretoken]'
  };

  // Кэш услуг
  const servicesCache = new Map();
  const CACHE_TIMEOUT = 5 * 60 * 1000; // 5 минут

  // Поиск элемента по составному селектору
  function findElement(selector) {
    const element = document.querySelector(selector);
    if (element) return element;
    
    const selectors = selector.split(', ');
    for (const singleSelector of selectors) {
      const el = document.querySelector(singleSelector.trim());
      if (el) return el;
    }
    return null;
  }

  // Получение конфигурации
  function getConfig() {
    const dataContainer = findElement(SELECTORS.ORDER_FORM_DATA);
    const csrfToken = findElement(SELECTORS.CSRF_TOKEN);
    
    return {
      servicesUrl: dataContainer?.dataset.servicesUrl || "/barbershop/masters_services/",
      csrfToken: csrfToken?.value || dataContainer?.dataset.csrfToken || ""
    };
  }

  // Кэширование
  function getCachedServices(masterId) {
    const cached = servicesCache.get(masterId);
    if (!cached || (Date.now() - cached.timestamp) > CACHE_TIMEOUT) {
      servicesCache.delete(masterId);
      return null;
    }
    return cached.data;
  }

  function setCachedServices(masterId, services) {
    servicesCache.set(masterId, {
      data: services,
      timestamp: Date.now()
    });
  }

  // Добавление опции в select
  function addOption(selectElement, text, value = "", disabled = false, selected = false) {
    const option = document.createElement("option");
    option.textContent = text;
    option.value = value;
    option.disabled = disabled;
    option.selected = selected;
    selectElement.appendChild(option);
  }

  // Установка состояния списка услуг
  function setServicesState(state, services = []) {
    const servicesSelect = findElement(SELECTORS.SERVICES_SELECT);
    if (!servicesSelect) return;
    
    servicesSelect.innerHTML = "";
    
    switch (state) {
      case 'loading':
        addOption(servicesSelect, "Загружаем услуги...", "", true, true);
        break;
      case 'disabled':
        addOption(servicesSelect, "Сначала выберите мастера", "", true, true);
        break;
      case 'error':
        addOption(servicesSelect, "У этого мастера нет услуг", "", true, true);
        break;
      case 'success':
        if (services.length === 0) {
          addOption(servicesSelect, "Выберите услуги", "", true, true);
        }
        services.forEach(service => {
          addOption(servicesSelect, service.name, service.id);
        });
        break;
    }
  }

  // Загрузка услуг с сервера
  async function fetchServices(masterId, servicesUrl, csrfToken) {
    try {
      const response = await fetch(servicesUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ master_id: masterId }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error("Ошибка при получении услуг:", error);
      return [];
    }
  }

  // Обновление списка услуг
  async function updateServicesDropdown(masterId) {
    if (!masterId) {
      setServicesState('disabled');
      return;
    }
    
    // Проверяем кэш
    const cachedServices = getCachedServices(masterId);
    if (cachedServices) {
      setServicesState(cachedServices.length > 0 ? 'success' : 'error', cachedServices);
      return;
    }
    
    // Загружаем с сервера
    setServicesState('loading');
    const { servicesUrl, csrfToken } = getConfig();
    const services = await fetchServices(masterId, servicesUrl, csrfToken);
    
    // Сохраняем в кэш
    setCachedServices(masterId, services);
    setServicesState(services.length > 0 ? 'success' : 'error', services);
  }

  // Обработчик изменения мастера
  function handleMasterChange(event) {
    updateServicesDropdown(event.target.value);
  }

  // Инициализация формы
  function initOrderForm() {
    const masterSelect = findElement(SELECTORS.MASTER_SELECT);
    const servicesSelect = findElement(SELECTORS.SERVICES_SELECT);
    
    if (!masterSelect || !servicesSelect) {
      console.error("Элементы формы не найдены");
      return;
    }
    
    masterSelect.addEventListener("change", handleMasterChange);
    
    // Инициализация состояния
    if (masterSelect.value) {
      updateServicesDropdown(masterSelect.value);
    } else {
      setServicesState('disabled');
    }
  }

  // Запуск при загрузке DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOrderForm);
  } else {
    initOrderForm();
  }

  console.log("Order form модуль загружен");
}
