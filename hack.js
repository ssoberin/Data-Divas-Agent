// Основной класс приложения для зимних работ
class WinterTerritoryManagementSystem {
    setupEventListeners() {
        
    // Мобильное меню с фоном
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });

        // Закрытие меню при клике на ссылку
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    hamburger.classList.remove('active');
                    navLinks.classList.remove('active');
                    document.body.classList.remove('menu-open');
                }
            });
        });

        // Закрытие меню при клике вне его
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && 
                !e.target.closest('.nav-links') && 
                !e.target.closest('.hamburger') &&
                navLinks.classList.contains('active')) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });

        // Закрытие меню при изменении размера окна
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });

        // Закрытие меню при нажатии Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    }

    // Остальные обработчики событий...
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            this.showSection(link.dataset.section);
        });
    });

    // ... остальной существующий код
}
    constructor() {
        this.tasks = JSON.parse(localStorage.getItem('winterTasks')) || [];
        this.currentSection = 'dashboard';
        this.disposalSites = {
            north: { name: 'Северный снегоприемник', capacity: 5000, current: 1200 },
            south: { name: 'Южный снегоприемник', capacity: 3000, current: 800 },
            east: { name: 'Восточный полигон', capacity: 4000, current: 1500 },
            west: { name: 'Западный карьер', capacity: 6000, current: 2000 }
        };
        this.init();
        this.analyticsData = {
            trucks: [
                { id: 1, name: 'Самосвал #001', driver: 'Иванов А.В.', workload: 90, trips: 5, volume: 45 },
                { id: 2, name: 'Самосвал #002', driver: 'Петров С.И.', workload: 65, trips: 3, volume: 32 },
                { id: 3, name: 'Самосвал #003', driver: 'Сидоров М.К.', workload: 40, trips: 2, volume: 20 },
                { id: 4, name: 'Самосвал #004', driver: 'Козлов Д.П.', workload: 85, trips: 4, volume: 42 }
            ],
            routes: [
                { name: 'Центр → Северный полигон', efficiency: 92 },
                { name: 'Парк → Южный полигон', efficiency: 78 },
                { name: 'Улицы → Восточный полигон', efficiency: 85 },
                { name: 'Парковки → Западный карьер', efficiency: 70 }
            ],
            timeData: [
                { time: '06:00', workload: 30 },
                { time: '08:00', workload: 65 },
                { time: '10:00', workload: 85 },
                { time: '12:00', workload: 90 },
                { time: '14:00', workload: 75 },
                { time: '16:00', workload: 60 },
                { time: '18:00', workload: 40 }
            ]
        };
        this.init();
    }

    init() {
        // ... существующий код ...
        this.setupAnalyticsEventListeners();
        this.updateAnalytics();
    }

    setupAnalyticsEventListeners() {
        // Обработчики для аналитики
        document.getElementById('refreshAnalytics').addEventListener('click', () => {
            this.refreshAnalytics();
        });

        document.getElementById('analyticsPeriod').addEventListener('change', () => {
            this.updateAnalytics();
        });
    }

    showSection(sectionName) {
        // ... существующий код ...
        if (sectionName === 'analytics') {
            this.updateAnalytics();
        }
    }

    refreshAnalytics() {
        // Имитация обновления данных
        this.showNotification('Данные аналитики обновлены');
        this.updateAnalytics();
    }

    updateAnalytics() {
        this.updateWorkloadStats();
        this.updateTruckWorkload();
        this.updateRouteEfficiency();
        this.updateTimeChart();
        this.updateKPIs();
    }

    updateWorkloadStats() {
        const avgWorkload = this.calculateAverageWorkload();
        const activeTrucks = this.analyticsData.trucks.length;
        const dailyTrips = this.analyticsData.trucks.reduce((sum, truck) => sum + truck.trips, 0);
        const downtimePercent = 100 - avgWorkload;

        document.getElementById('avgWorkload').textContent = `${avgWorkload}%`;
        document.getElementById('activeTrucks').textContent = activeTrucks;
        document.getElementById('dailyTrips').textContent = dailyTrips;
        document.getElementById('downtimePercent').textContent = `${downtimePercent}%`;
    }

    calculateAverageWorkload() {
        const total = this.analyticsData.trucks.reduce((sum, truck) => sum + truck.workload, 0);
        return Math.round(total / this.analyticsData.trucks.length);
    }

    updateTruckWorkload() {
        const workloadList = document.querySelector('.workload-list');
        if (!workloadList) return;

        workloadList.innerHTML = this.analyticsData.trucks.map(truck => {
            const workloadClass = this.getWorkloadClass(truck.workload);
            return `
                <div class="workload-item">
                    <div class="truck-info">
                        <span class="truck-id">${truck.name}</span>
                        <span class="truck-driver">${truck.driver}</span>
                    </div>
                    <div class="workload-bar">
                        <div class="workload-fill ${workloadClass}" style="width: ${truck.workload}%">
                            <span class="workload-text">${truck.workload}%</span>
                        </div>
                    </div>
                    <div class="workload-stats">
                        <span>${truck.trips} рейсов</span>
                        <span>${truck.volume} м³</span>
                    </div>
                </div>
            `;
        }).join('');
    }

    getWorkloadClass(workload) {
        if (workload >= 80) return 'high';
        if (workload >= 60) return 'medium';
        return 'low';
    }

    updateRouteEfficiency() {
        const routeEfficiency = document.querySelector('.route-efficiency');
        if (!routeEfficiency) return;

        routeEfficiency.innerHTML = this.analyticsData.routes.map(route => `
            <div class="efficiency-item">
                <span class="route-name">${route.name}</span>
                <div class="efficiency-bar">
                    <div class="efficiency-fill" style="width: ${route.efficiency}%"></div>
                </div>
                <span class="efficiency-value">${route.efficiency}%</span>
            </div>
        `).join('');
    }

    updateTimeChart() {
        const chartBars = document.querySelector('.chart-bars');
        if (!chartBars) return;

        chartBars.innerHTML = this.analyticsData.timeData.map(data => `
            <div class="time-bar">
                <div class="time-label">${data.time}</div>
                <div class="bar-container">
                    <div class="bar-fill" style="height: ${data.workload}%"></div>
                </div>
                <div class="bar-value">${data.workload}%</div>
            </div>
        `).join('');
    }

    updateKPIs() {
        // Расчет KPI на основе данных
        const avgTripTime = '2.3 ч';
        const avgLoad = '18.5 м³';
        const avgDistance = '23 км';
        const avgFuel = '28 л';

        // Здесь можно добавить логику обновления KPI, если они будут динамическими
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.updateDashboard();
        this.renderTasks();
        this.setupReports();
    }

    setupEventListeners() {
        // Навигация
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.showSection(link.dataset.section);
            });
        });

        // Мобильное меню
        document.querySelector('.hamburger').addEventListener('click', () => {
            document.querySelector('.nav-links').classList.toggle('active');
        });

        // Модальное окно
        document.getElementById('showTaskModal').addEventListener('click', () => {
            this.showModal();
        });

        document.querySelector('.close').addEventListener('click', () => {
            this.hideModal();
        });

        document.getElementById('cancelTask').addEventListener('click', () => {
            this.hideModal();
        });

        // Форма задачи
        document.getElementById('taskForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTask();
        });

        // Быстрая форма
        document.getElementById('quickTaskForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addQuickTask(e.target);
        });

        // Фильтры
        document.getElementById('filterStatus').addEventListener('change', () => {
            this.renderTasks();
        });

        document.getElementById('filterPriority').addEventListener('change', () => {
            this.renderTasks();
        });

        document.getElementById('filterArea').addEventListener('change', () => {
            this.renderTasks();
        });

        document.getElementById('filterSnowType').addEventListener('change', () => {
            this.renderTasks();
        });

        // Оптимизация маршрута
        document.getElementById('optimizeRoute').addEventListener('click', () => {
            this.optimizeSnowRoute();
        });

        // Назначение маршрута
        document.getElementById('assignRoute').addEventListener('click', () => {
            this.assignSnowRoute();
        });

        // Погода
        document.getElementById('updateWeather').addEventListener('click', () => {
            this.updateWeatherData();
        });

        document.getElementById('weatherForecast').addEventListener('click', () => {
            this.showWeatherForecast();
        });

        // Отчеты
        document.getElementById('generateReport').addEventListener('click', () => {
            this.generateWinterReport();
        });

        document.getElementById('exportPDF').addEventListener('click', () => {
            this.exportWinterPDF();
        });

        // Документы
        document.getElementById('generateDocs').addEventListener('click', () => {
            this.generateWinterDocuments();
        });

        // Карта
        document.querySelectorAll('.map-zone').forEach(zone => {
            zone.addEventListener('click', () => {
                this.showZoneSnowTasks(zone.dataset.zone);
            });
        });

        document.getElementById('showSnowAccumulation').addEventListener('click', () => {
            this.showSnowAccumulation();
        });

        document.getElementById('showClearedZones').addEventListener('click', () => {
            this.showClearedZones();
        });

        document.getElementById('showRoute').addEventListener('click', () => {
            this.showSnowRoute();
        });

        // Закрытие модального окна при клике вне его
        window.addEventListener('click', (event) => {
            const modal = document.getElementById('taskModal');
            if (event.target === modal) {
                this.hideModal();
            }
        });

        // Закрытие мобильного меню при клике вне его
        window.addEventListener('click', (event) => {
            const nav = document.querySelector('.nav');
            const hamburger = document.querySelector('.hamburger');
            
            if (!nav.contains(event.target) && !hamburger.contains(event.target)) {
                document.querySelector('.nav-links').classList.remove('active');
            }
        });
    }

    showSection(sectionName) {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        document.getElementById(sectionName).classList.add('active');
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        this.currentSection = sectionName;

        if (sectionName === 'dashboard') {
            this.updateDashboard();
        } else if (sectionName === 'tasks') {
            this.renderTasks();
        } else if (sectionName === 'reports') {
            this.updateReports();
        }
    }

    showModal() {
        document.getElementById('taskModal').style.display = 'block';
        document.getElementById('taskDate').min = new Date().toISOString().split('T')[0];
    }

    hideModal() {
        document.getElementById('taskModal').style.display = 'none';
        document.getElementById('taskForm').reset();
    }

    addTask() {
        const formData = {
            id: Date.now(),
            type: document.getElementById('taskType').value,
            priority: document.getElementById('taskPriority').value,
            description: document.getElementById('taskDescription').value,
            area: document.getElementById('taskArea').value,
            snowVolume: parseInt(document.getElementById('snowVolume').value),
            date: document.getElementById('taskDate').value,
            duration: parseInt(document.getElementById('taskDuration').value),
            equipment: Array.from(document.querySelectorAll('input[name="equipment"]:checked')).map(cb => cb.value),
            disposalSite: document.getElementById('disposalSite').value,
            status: 'pending',
            createdAt: new Date().toISOString(),
            completed: false
        };

        this.tasks.push(formData);
        this.saveTasks();
        this.renderTasks();
        this.updateDashboard();
        this.hideModal();
        this.showNotification('Задача по снегу успешно добавлена!');
    }

    addQuickTask(form) {
        const quickTask = {
            id: Date.now(),
            type: document.getElementById('quickTaskType').value,
            priority: 'medium',
            description: `Быстрая задача: ${this.getSnowTypeText(document.getElementById('quickTaskType').value)}`,
            area: document.getElementById('quickTaskArea').value,
            snowVolume: parseInt(document.getElementById('quickSnowVolume').value) || 10,
            date: new Date().toISOString().split('T')[0],
            duration: 2,
            equipment: ['snowplow'],
            disposalSite: 'north',
            status: 'pending',
            createdAt: new Date().toISOString(),
            completed: false
        };

        this.tasks.push(quickTask);
        this.saveTasks();
        this.renderTasks();
        this.updateDashboard();
        form.reset();
        this.showNotification('Зимняя задача добавлена в план!');
    }

    renderTasks() {
        const tasksList = document.getElementById('tasksList');
        const statusFilter = document.getElementById('filterStatus').value;
        const priorityFilter = document.getElementById('filterPriority').value;
        const areaFilter = document.getElementById('filterArea').value;
        const snowTypeFilter = document.getElementById('filterSnowType').value;

        let filteredTasks = this.tasks.filter(task => {
            const statusMatch = statusFilter === 'all' || 
                (statusFilter === 'completed' && task.completed) ||
                (statusFilter === 'in-progress' && task.status === 'in-progress' && !task.completed) ||
                (statusFilter === 'pending' && task.status === 'pending' && !task.completed);
            
            const priorityMatch = priorityFilter === 'all' || task.priority === priorityFilter;
            const areaMatch = areaFilter === 'all' || task.area === areaFilter;
            const snowTypeMatch = snowTypeFilter === 'all' || task.type === snowTypeFilter;
            
            return statusMatch && priorityMatch && areaMatch && snowTypeMatch;
        });

        filteredTasks.sort((a, b) => {
            if (a.completed !== b.completed) {
                return a.completed ? 1 : -1;
            }
            
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            const today = new Date();
            
            if (dateA < today && dateB >= today) return -1;
            if (dateB < today && dateA >= today) return 1;
            
            const priorityOrder = { emergency: 4, high: 3, medium: 2, low: 1 };
            if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
                return priorityOrder[b.priority] - priorityOrder[a.priority];
            }
            
            return dateA - dateB;
        });

        if (filteredTasks.length === 0) {
            tasksList.innerHTML = '<div class="card"><p>Задачи по снегу не найдены</p></div>';
            return;
        }

        tasksList.innerHTML = filteredTasks.map(task => this.createSnowTaskCard(task)).join('');
        this.attachTaskEventHandlers();
    }

    createSnowTaskCard(task) {
        const snowTypes = {
            snow_removal: { text: 'Уборка снега', icon: '🏔️' },
            snow_loading: { text: 'Погрузка снега', icon: '📦' },
            snow_transport: { text: 'Вывоз снега', icon: '🚛' },
            ice_removal: { text: 'Удаление наледи', icon: '🧊' },
            sanding: { text: 'Песчаная посыпка', icon: '🪣' }
        };

        const areas = {
            main_streets: 'Основные улицы',
            secondary_streets: 'Второстепенные улицы',
            pedestrian_zones: 'Пешеходные зоны',
            parking: 'Парковки',
            entrances: 'Подъездные пути'
        };

        const priorities = {
            emergency: { text: 'Аварийный', class: 'priority-emergency' },
            high: { text: 'Высокий', class: 'priority-high' },
            medium: { text: 'Средний', class: 'priority-medium' },
            low: { text: 'Низкий', class: 'priority-low' }
        };

        const isOverdue = new Date(task.date) < new Date() && !task.completed;

        return `
            <div class="task-card ${task.completed ? 'task-completed' : ''}" data-id="${task.id}">
                <div class="task-header">
                    <h3>${snowTypes[task.type].icon} ${task.description || snowTypes[task.type].text}</h3>
                    <span class="${priorities[task.priority].class}">${priorities[task.priority].text}</span>
                </div>
                <div class="task-meta">
                    <span class="area-badge">${areas[task.area]}</span>
                    <span>Объем: ${task.snowVolume} м³</span>
                    <span>Срок: ${this.formatDate(task.date)}</span>
                    <span>Время: ${task.duration} ч</span>
                    ${isOverdue ? '<span class="priority-emergency">ПРОСРОЧЕНО</span>' : ''}
                    ${task.completed ? '<span class="priority-low">ВЫПОЛНЕНО</span>' : ''}
                </div>
                <div class="task-equipment">
                    <strong>Техника:</strong> ${task.equipment.map(eq => this.getEquipmentText(eq)).join(', ')}
                </div>
                <div class="task-disposal">
                    <strong>Полигон:</strong> ${this.disposalSites[task.disposalSite].name}
                </div>
                <div class="task-actions">
                    ${!task.completed ? 
                        `<button class="btn-primary" onclick="app.startTask(${task.id})">Начать работу</button>
                         <button class="btn-success" onclick="app.completeTask(${task.id})">Завершить</button>` : 
                        `<button class="btn-secondary" onclick="app.reopenTask(${task.id})">Возобновить</button>`
                    }
                    <button class="btn-danger" onclick="app.deleteTask(${task.id})">Удалить</button>
                </div>
            </div>
        `;
    }

    attachTaskEventHandlers() {
        // Обработчики уже добавлены в createTaskCard через onclick
    }

    getSnowTypeText(type) {
        const types = {
            snow_removal: 'Уборка снега',
            snow_loading: 'Погрузка снега',
            snow_transport: 'Вывоз снега',
            ice_removal: 'Удаление наледи',
            sanding: 'Песчаная посыпка'
        };
        return types[type] || type;
    }

    getEquipmentText(equipment) {
        const equipmentNames = {
            snowplow: 'Снегоуборочная машина',
            loader: 'Погрузчик',
            truck: 'Самосвал',
            spreader: 'Песчаница'
        };
        return equipmentNames[equipment] || equipment;
    }

    startTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (task) {
            task.status = 'in-progress';
            this.saveTasks();
            this.renderTasks();
            this.showNotification(`Задача "${this.getSnowTypeText(task.type)}" начата`);
        }
    }

    completeTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (task) {
            task.status = 'completed';
            task.completed = true;
            task.completedAt = new Date().toISOString();
            this.saveTasks();
            this.renderTasks();
            this.updateDashboard();
            this.showNotification(`Задача "${this.getSnowTypeText(task.type)}" завершена`);
        }
    }

    reopenTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (task) {
            task.status = 'pending';
            task.completed = false;
            delete task.completedAt;
            this.saveTasks();
            this.renderTasks();
            this.updateDashboard();
            this.showNotification(`Задача "${this.getSnowTypeText(task.type)}" возобновлена`);
        }
    }

    deleteTask(taskId) {
        if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
            this.tasks = this.tasks.filter(task => task.id !== taskId);
            this.saveTasks();
            this.renderTasks();
            this.updateDashboard();
            this.showNotification('Задача удалена');
        }
    }

    optimizeSnowRoute() {
        const activeTasks = this.tasks.filter(task => !task.completed && task.type === 'snow_transport');
        
        if (activeTasks.length === 0) {
            this.showNotification('Нет задач по вывозу снега для построения маршрута');
            return;
        }

        const optimizedTasks = [...activeTasks].sort((a, b) => {
            const priorityOrder = { emergency: 4, high: 3, medium: 2, low: 1 };
            if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
                return priorityOrder[b.priority] - priorityOrder[a.priority];
            }
            
            return new Date(a.date) - new Date(b.date);
        });

        this.displaySnowRoute(optimizedTasks);
        this.showNotification('Маршрут вывоза снега оптимизирован');
    }

    displaySnowRoute(tasks) {
        const routeVisualization = document.getElementById('routeVisualization');
        const suggestedRoute = document.getElementById('suggestedRoute');
        
        const areas = {
            main_streets: 'Основные улицы',
            secondary_streets: 'Второстепенные улицы',
            pedestrian_zones: 'Пешеходные зоны',
            parking: 'Парковки',
            entrances: 'Подъездные пути'
        };

        const totalVolume = tasks.reduce((sum, task) => sum + task.snowVolume, 0);
        const totalTrips = Math.ceil(totalVolume / 20); // Предполагаем 20 м³ за рейс

        routeVisualization.innerHTML = `
            <h4>Оптимальный маршрут вывоза снега:</h4>
            <div class="route-steps">
                ${tasks.map((task, index) => `
                    <div class="route-step">
                        <strong>${index + 1}. ${areas[task.area]}</strong>
                        <span>${task.snowVolume} м³ → ${this.disposalSites[task.disposalSite].name}</span>
                    </div>
                `).join('')}
            </div>
        `;

        suggestedRoute.innerHTML = tasks.slice(0, 5).map((task, index) => 
            `<li>${areas[task.area]} - ${task.snowVolume} м³</li>`
        ).join('');

        document.getElementById('totalSnowVolume').textContent = totalVolume;
        document.getElementById('totalTrips').textContent = totalTrips;
        document.getElementById('currentDisposalSite').textContent = tasks[0] ? this.disposalSites[tasks[0].disposalSite].name : 'Не выбран';
        document.getElementById('disposalSite').textContent = tasks[0] ? this.disposalSites[tasks[0].disposalSite].name : 'Не выбран';
    }

    assignSnowRoute() {
        this.showNotification('Маршрут вывоза снега назначен водителям');
    }

    updateDashboard() {
        const now = new Date();
        const today = now.toISOString().split('T')[0];
        
        const snowTasks = this.tasks.filter(task => 
            ['snow_removal', 'snow_loading', 'snow_transport'].includes(task.type)
        );
        
        const completedToday = this.tasks.filter(task => 
            task.completed && task.completedAt && task.completedAt.startsWith(today)
        );
        
        const snowVolumeToday = completedToday.reduce((sum, task) => sum + (task.snowVolume || 0), 0);
        const activeSnowTasks = snowTasks.filter(task => !task.completed).length;

        const totalTasks = this.tasks.length;
        const completedTasks = this.tasks.filter(task => task.completed).length;
        const efficiency = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

        document.getElementById('snowRemovedCount').textContent = `${snowVolumeToday} м³`;
        document.getElementById('activeMachinesCount').textContent = '3'; // Статичные данные для примера
        document.getElementById('snowTasksCount').textContent = activeSnowTasks;
        document.getElementById('efficiencyPercent').textContent = `${efficiency}%`;

        this.updateUrgentTasks();
        this.optimizeSnowRoute();
    }

    updateUrgentTasks() {
        const urgentTasksList = document.getElementById('urgentTasksList');
        const urgentTasks = this.tasks.filter(task => 
            !task.completed && 
            (task.priority === 'emergency' || new Date(task.date) < new Date())
        ).slice(0, 3);

        if (urgentTasks.length === 0) {
            urgentTasksList.innerHTML = '<p>Нет срочных задач по снегу</p>';
            return;
        }

        urgentTasksList.innerHTML = urgentTasks.map(task => `
            <div class="urgent-task">
                <strong>${this.getSnowTypeText(task.type)}</strong>
                <p>${this.getAreaText(task.area)} | ${task.snowVolume} м³</p>
                <small>${this.formatDate(task.date)}</small>
            </div>
        `).join('');
    }

    getAreaText(area) {
        const areas = {
            main_streets: 'Основные улицы',
            secondary_streets: 'Второстепенные улицы',
            pedestrian_zones: 'Пешеходные зоны',
            parking: 'Парковки',
            entrances: 'Подъездные пути'
        };
        return areas[area] || area;
    }

    setupReports() {
        this.updateReports();
    }

    updateReports() {
        this.createSnowWorkChart();
        this.createWorkTypesChart();
        this.updateSnowStats();
    }

    createSnowWorkChart() {
        const snowWorkChart = document.getElementById('snowWorkChart');
        
        const completed = this.tasks.filter(task => task.completed).length;
        const pending = this.tasks.filter(task => !task.completed).length;
        const total = completed + pending;
        
        const completedPercent = total > 0 ? Math.round((completed / total) * 100) : 0;
        const pendingPercent = total > 0 ? Math.round((pending / total) * 100) : 0;

        snowWorkChart.innerHTML = `
            <div class="chart-bar">
                <div class="chart-label">Выполнено</div>
                <div class="chart-value">
                    <div class="chart-fill" style="width: ${completedPercent}%"></div>
                    <span class="chart-percentage">${completed} (${completedPercent}%)</span>
                </div>
            </div>
            <div class="chart-bar">
                <div class="chart-label">В работе</div>
                <div class="chart-value">
                    <div class="chart-fill" style="width: ${pendingPercent}%"></div>
                    <span class="chart-percentage">${pending} (${pendingPercent}%)</span>
                </div>
            </div>
        `;
    }

    createWorkTypesChart() {
        const workTypesChart = document.getElementById('workTypesChart');
        
        const snowTypes = ['snow_removal', 'snow_loading', 'snow_transport', 'ice_removal', 'sanding'];
        const typeNames = {
            snow_removal: 'Уборка снега',
            snow_loading: 'Погрузка снега',
            snow_transport: 'Вывоз снега',
            ice_removal: 'Удаление наледи',
            sanding: 'Песчаная посыпка'
        };
        
        const typeCounts = {};
        snowTypes.forEach(type => {
            typeCounts[type] = this.tasks.filter(task => task.type === type).length;
        });
        
        const total = Object.values(typeCounts).reduce((sum, count) => sum + count, 0);
        
        workTypesChart.innerHTML = `
            <div class="pie-chart">
                ${snowTypes.map(type => {
                    const count = typeCounts[type];
                    const percent = total > 0 ? Math.round((count / total) * 100) : 0;
                    const color = this.getChartColor(type);
                    return `
                        <div class="pie-segment" style="background: ${color}" title="${typeNames[type]}: ${count} (${percent}%)">
                            ${typeNames[type].split(' ')[0]}<br>${percent}%
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    getChartColor(type) {
        const colors = {
            snow_removal: '#2196f3',
            snow_loading: '#ff9800',
            snow_transport: '#4caf50',
            ice_removal: '#9c27b0',
            sanding: '#ffeb3b'
        };
        return colors[type] || '#cccccc';
    }

    updateSnowStats() {
        const statsBody = document.getElementById('snowStats');
        
        const totalSnowVolume = this.tasks.reduce((sum, task) => sum + (task.snowVolume || 0), 0);
        const completedVolume = this.tasks
            .filter(task => task.completed)
            .reduce((sum, task) => sum + (task.snowVolume || 0), 0);
        
        const today = new Date().toISOString().split('T')[0];
        const completedToday = this.tasks.filter(task => 
            task.completed && task.completedAt && task.completedAt.startsWith(today)
        ).length;
        
        statsBody.innerHTML = `
            <tr>
                <td>Всего снега для уборки</td>
                <td>${totalSnowVolume} м³</td>
                <td>+150 м³</td>
            </tr>
            <tr>
                <td>Уже вывезено</td>
                <td>${completedVolume} м³</td>
                <td>+80 м³</td>
            </tr>
            <tr>
                <td>Задач выполнено сегодня</td>
                <td>${completedToday}</td>
                <td>+3</td>
            </tr>
        `;
    }

    // Методы для работы с погодой
    updateWeatherData() {
        this.showNotification('Данные о погоде обновлены');
        // В реальной системе здесь был бы API запрос к метеосервису
    }

    showWeatherForecast() {
        this.showNotification('Загружен прогноз погоды на 3 дня');
        // В реальной системе здесь было бы отображение прогноза
    }

    // Методы для отчетов и документов
    generateWinterReport() {
        this.showNotification('Зимний отчет сформирован');
    }

    exportWinterPDF() {
        this.showNotification('PDF документ по зимним работам готов к скачиванию');
    }

    generateWinterDocuments() {
        this.showNotification('Пакет зимних документов сформирован');
    }

    previewDocument(docType) {
        this.showNotification(`Предпросмотр документа: ${this.getDocumentName(docType)}`);
    }

    downloadDocument(docType) {
        this.showNotification(`Документ "${this.getDocumentName(docType)}" готов к скачиванию`);
    }

    getDocumentName(docType) {
        const names = {
            snow_act: 'Акт вывоза снега',
            winter_journal: 'Журнал зимнего содержания',
            anti_icing_plan: 'План противоскользящих мероприятий'
        };
        return names[docType] || docType;
    }

    // Методы для карты
    showZoneSnowTasks(zone) {
        const zoneTasks = this.tasks.filter(task => task.area === zone && !task.completed);
        alert(`Задачи по снегу в зоне "${this.getAreaText(zone)}": ${zoneTasks.length}`);
    }

    showSnowAccumulation() {
        this.showNotification('Показаны зоны снежных накоплений');
    }

    showClearedZones() {
        this.showNotification('Показаны очищенные от снега зоны');
    }

    showSnowRoute() {
        this.showNotification('Маршрут вывоза снега отображен на карте');
    }

    // Вспомогательные методы
    formatDate(dateString) {
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
        return new Date(dateString).toLocaleDateString('ru-RU', options);
    }

    showNotification(message) {
        // Создаем элемент уведомления
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4caf50;
            color: white;
            padding: 15px 20px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1001;
            transform: translateX(150%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Анимация появления
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Автоматическое скрытие
        setTimeout(() => {
            notification.style.transform = 'translateX(150%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    saveTasks() {
        localStorage.setItem('winterTasks', JSON.stringify(this.tasks));
    }

    loadInitialData() {
        if (this.tasks.length === 0) {
            this.tasks = [
                {
                    id: 1,
                    type: 'snow_removal',
                    priority: 'high',
                    description: 'Уборка снега с центральных улиц',
                    area: 'main_streets',
                    snowVolume: 50,
                    date: new Date().toISOString().split('T')[0],
                    duration: 4,
                    equipment: ['snowplow'],
                    disposalSite: 'north',
                    status: 'pending',
                    completed: false,
                    createdAt: new Date().toISOString()
                },
                {
                    id: 2,
                    type: 'snow_transport',
                    priority: 'emergency',
                    description: 'Срочный вывоз снега с парковки',
                    area: 'parking',
                    snowVolume: 30,
                    date: new Date().toISOString().split('T')[0],
                    duration: 2,
                    equipment: ['loader', 'truck'],
                    disposalSite: 'south',
                    status: 'in-progress',
                    completed: false,
                    createdAt: new Date().toISOString()
                },
                {
                    id: 3,
                    type: 'ice_removal',
                    priority: 'high',
                    description: 'Удаление наледи с пешеходных зон',
                    area: 'pedestrian_zones',
                    snowVolume: 0,
                    date: new Date().toISOString().split('T')[0],
                    duration: 3,
                    equipment: ['spreader'],
                    disposalSite: 'north',
                    status: 'pending',
                    completed: false,
                    createdAt: new Date().toISOString()
                }
            ];
            this.saveTasks();
        }
    }
    
}

// Инициализация приложения
const app = new WinterTerritoryManagementSystem();

// Сделаем app глобальной для обработчиков onclick в HTML
window.app = app;