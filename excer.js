// Массив для хранения задач
let tasks = [];

// Функция обработки задач ИИ
function processTask() {
    const input = document.getElementById('task-input').value;
    const tableBody = document.querySelector('#task-table tbody');
    
    // Имитация работы ИИ - разбиваем ввод по разделителям
    tasks = input.split(';').map(task => {
        const parts = task.split('/');
        return {
            area: parts[0] || '',
            responsible: parts[1] || '',
            phone: parts[2] || '',
            mode: parts[3] || '',
            time: parts[4] || '',
            techType: parts[5] || '',
            quantity: parts[6] || '',
            plan: parts[7] || '',
            workType: parts[8] || ''
        };
    });

    tableBody.innerHTML = '';
    
    tasks.forEach(task => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${task.area}</td>
            <td>${task.responsible}</td>
            <td>${task.phone}</td>
            <td>${task.mode}</td>
            <td>${task.time}</td>
            <td>${task.techType}</td>
            <td>${task.quantity}</td>
            <td>${task.plan}</td>
            <td>${task.workType}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Функция поиска задач
function searchTask() {
    const keyword = document.getElementById('task-search').value.toLowerCase();
    const rows = document.querySelectorAll('#task-table tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(keyword) ? '' : 'none';
    });
}

// Функция экспорта задач в CSV
function exportTasksToCSV() {
    if (tasks.length === 0) {
        showNotification('Нет данных для экспорта', 'warning');
        return;
    }
    
    const headers = ['Участок', 'Ответственный', 'Телефон', 'Режим', 'Время', 'Тип техники', 'Количество', 'Плановое задание', 'Вид работ'];
    
    let csvContent = headers.join(',') + '\n';
    
    tasks.forEach(task => {
        const row = [
            task.area,
            task.responsible,
            task.phone,
            task.mode,
            task.time,
            task.techType,
            task.quantity,
            task.plan,
            task.workType
        ];
        csvContent += row.join(',') + '\n';
    });
    
    downloadCSV(csvContent, 'tasks_export.csv');
    showNotification('Задачи успешно экспортированы в CSV', 'success');
}

// Вспомогательная функция для скачивания CSV
function downloadCSV(csvContent, filename) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Функция переключения вкладок
function openTab(tabName) {
    // Скрыть все вкладки
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    // Убрать активный класс со всех кнопок
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    // Показать выбранную вкладку и активировать кнопку
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Функция отправки данных формы учета работ
function submitWorkData() {
    const depot = document.getElementById('depot').value;
    const workerName = document.getElementById('worker-name').value;
    const machineType = document.getElementById('machine-type').value;
    const bodyVolume = document.getElementById('body-volume').value;
    const maxCapacity = document.getElementById('max-capacity').value;
    const snowCapacity = document.getElementById('snow-capacity').value;
    
    // Проверка заполнения всех полей
    if (!depot || !workerName || !machineType || !bodyVolume || !maxCapacity || !snowCapacity) {
        showNotification('Заполните все поля формы', 'error');
        return;
    }
    
    // Проверка числовых значений
    if (bodyVolume <= 0 || maxCapacity <= 0 || snowCapacity <= 0) {
        showNotification('Числовые значения должны быть больше 0', 'error');
        return;
    }
    
    // Создаем объект с данными
    const workData = {
        id: Date.now(),
        date: new Date().toLocaleDateString('ru-RU'),
        time: new Date().toLocaleTimeString('ru-RU'),
        depot: depot,
        workerName: workerName,
        machineType: machineType,
        bodyVolume: parseFloat(bodyVolume),
        maxCapacity: parseFloat(maxCapacity),
        snowCapacity: parseFloat(snowCapacity)
    };
    
    // Здесь можно добавить отправку данных на сервер
    // Например: sendToServer(workData);
    
    // Сохраняем в localStorage для примера
    saveWorkData(workData);
    
    // Показываем уведомление об успешной отправке
    showNotification('Данные успешно отправлены!', 'success');
    
    // Очищаем форму
    clearWorkForm();
}

// Функция сохранения данных в localStorage
function saveWorkData(data) {
    let workHistory = JSON.parse(localStorage.getItem('workHistory')) || [];
    workHistory.push(data);
    localStorage.setItem('workHistory', JSON.stringify(workHistory));
}

// Функция очистки формы
function clearWorkForm() {
    document.getElementById('depot').value = '';
    document.getElementById('worker-name').value = '';
    document.getElementById('machine-type').value = '';
    document.getElementById('body-volume').value = '';
    document.getElementById('max-capacity').value = '';
    document.getElementById('snow-capacity').value = '';
}

// Функция показа уведомления
function showNotification(message, type = 'success') {
    // Удаляем предыдущее уведомление, если есть
    const oldNotification = document.querySelector('.notification');
    if (oldNotification) {
        oldNotification.remove();
    }
    
    // Создаем новое уведомление
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    
    // Настраиваем цвет в зависимости от типа
    if (type === 'error') {
        notification.style.background = '#dc3545';
    } else if (type === 'warning') {
        notification.style.background = '#ffc107';
        notification.style.color = '#333';
    } else {
        notification.style.background = '#28a745';
    }
    
    // Добавляем уведомление на страницу
    document.body.appendChild(notification);
    
    // Показываем уведомление
    notification.style.display = 'block';
    
    // Автоматически скрываем через 3 секунды
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Можно добавить инициализацию данных, если нужно
    console.log('Система учета загружена');
    
    // Устанавливаем минимальную дату в поле даты (если бы оно было)
    const today = new Date().toISOString().split('T')[0];
    
    // Загружаем историю из localStorage (для примера)
    const workHistory = JSON.parse(localStorage.getItem('workHistory')) || [];
    console.log('История работ:', workHistory);
});
