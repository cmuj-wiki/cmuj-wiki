/**
 * Homepage "Co Dalej?" Widget
 *
 * Displays upcoming classes and kolokwia for the user's selected group
 * Uses localStorage to remember user's group selection
 */

(function() {
    'use strict';

    // Configuration
    const STORAGE_KEY = 'cmuj_user_group';
    const WIDGET_ID = 'co-dalej-widget';

    // Initialize widget when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }

    // Re-initialize on instant navigation (MkDocs Material)
    document.addEventListener('DOMContentLoaded', function() {
        // Listen for Material's navigation events
        if (typeof document$ !== 'undefined') {
            document$.subscribe(function() {
                initWidget();
            });
        }
    });

    function initWidget() {
        const widgetContainer = document.getElementById(WIDGET_ID);
        if (!widgetContainer) return; // Widget only on homepage

        renderWidget(widgetContainer);
    }

    function renderWidget(container) {
        const userGroup = getUserGroup();

        if (!userGroup) {
            // Show group selection prompt
            container.innerHTML = renderGroupSelector();
            attachGroupSelectorListeners(container);
        } else {
            // Show personalized content
            container.innerHTML = renderPersonalizedContent(userGroup);
            attachWidgetListeners(container);
        }
    }

    function getUserGroup() {
        return localStorage.getItem(STORAGE_KEY);
    }

    function setUserGroup(group) {
        localStorage.setItem(STORAGE_KEY, group);
    }

    function renderGroupSelector() {
        return `
            <div class="widget-group-selector">
                <h3>👋 Witaj na CMUJ Wiki!</h3>
                <p>Wybierz swoją grupę zajęciową, aby zobaczyć spersonalizowany harmonogram:</p>

                <div class="group-grid">
                    ${Array.from({length: 20}, (_, i) => i + 1).map(num => `
                        <button class="group-btn" data-group="${num}">
                            Grupa ${num}
                        </button>
                    `).join('')}
                </div>

                <p class="widget-note">
                    💡 Twój wybór zostanie zapamiętany w przeglądarce
                </p>
            </div>
        `;
    }

    function renderPersonalizedContent(group) {
        const upcomingEvents = getUpcomingEvents(group);
        const nextWeekClasses = getNextWeekClasses(group);

        return `
            <div class="widget-header">
                <h3>📅 Co dalej? <span class="widget-group-badge">Grupa ${group}</span></h3>
                <button class="widget-change-group" id="change-group-btn">
                    Zmień grupę
                </button>
            </div>

            <div class="widget-content">
                <!-- Upcoming Kolokwia -->
                <div class="widget-section widget-kolokwia">
                    <h4>🎯 Nadchodzące kolokwia i egzaminy</h4>
                    ${upcomingEvents.length > 0 ? `
                        <div class="event-list">
                            ${upcomingEvents.map(event => renderEvent(event)).join('')}
                        </div>
                    ` : `
                        <p class="widget-empty">Brak nadchodzących kolokwiów w najbliższym czasie</p>
                    `}
                    <a href="kolokwia/index.html" class="widget-link">Zobacz wszystkie kolokwia →</a>
                </div>

                <!-- Next Week Classes -->
                <div class="widget-section widget-classes">
                    <h4>📚 Zajęcia w tym tygodniu</h4>
                    ${nextWeekClasses.length > 0 ? `
                        <div class="class-list">
                            ${nextWeekClasses.map(cls => renderClass(cls)).join('')}
                        </div>
                    ` : `
                        <p class="widget-empty">Brak zajęć do wyświetlenia</p>
                    `}
                    <a href="kalendarz/index.html" class="widget-link">Zobacz kalendarz (BETA) →</a>
                </div>
            </div>
        `;
    }

    function renderEvent(event) {
        const daysUntil = getDaysUntil(event.date);
        const urgencyClass = daysUntil <= 7 ? 'urgent' : daysUntil <= 14 ? 'soon' : '';

        return `
            <div class="event-card ${urgencyClass}">
                <div class="event-date">
                    <div class="event-countdown">${daysUntil === 0 ? 'Dziś!' : daysUntil === 1 ? 'Jutro' : `Za ${daysUntil} dni`}</div>
                    <div class="event-date-full">${formatDate(event.date)}</div>
                </div>
                <div class="event-details">
                    <div class="event-subject">${event.subject}</div>
                    <div class="event-type">${event.type}</div>
                    ${event.topic ? `<div class="event-topic">${event.topic}</div>` : ''}
                </div>
                ${event.link ? `<a href="${event.link}" class="event-link">Przygotuj się →</a>` : ''}
            </div>
        `;
    }

    function renderClass(cls) {
        return `
            <div class="class-item">
                <div class="class-day">${cls.day}</div>
                <div class="class-time">${cls.time}</div>
                <div class="class-subject">${cls.subject}</div>
                ${cls.type ? `<span class="class-type-badge">${cls.type}</span>` : ''}
            </div>
        `;
    }

    function attachGroupSelectorListeners(container) {
        const buttons = container.querySelectorAll('.group-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', function() {
                const group = this.dataset.group;
                setUserGroup(group);
                renderWidget(container);
            });
        });
    }

    function attachWidgetListeners(container) {
        const changeBtn = container.querySelector('#change-group-btn');
        if (changeBtn) {
            changeBtn.addEventListener('click', function() {
                localStorage.removeItem(STORAGE_KEY);
                renderWidget(container);
            });
        }
    }

    function getUpcomingEvents(group) {
        // TODO: Load from schedule_data_v2.json and exam_dates.json
        // For now, return hardcoded upcoming events from data/exam_dates_manual.yml

        const today = new Date();
        const events = [
            {
                date: '2025-11-06',
                subject: 'Anatomia',
                type: 'Kolokwium praktyczne',
                topic: 'Osteologia i czaszka',
                groups: [1, 2, 3, 4],
                link: 'kolokwia/semestr-1/anatomia-kolokwia-1.html'
            },
            {
                date: '2025-11-18',
                subject: 'Anatomia',
                type: 'Kolokwium testowe',
                topic: 'Kości, czaszka',
                groups: [1, 2, 3, 4],
                link: 'kolokwia/semestr-1/anatomia-kolokwia-2.html'
            },
            {
                date: '2025-11-20',
                subject: 'Histologia',
                type: 'Kolokwium',
                topic: 'Cytologia i tkanki',
                groups: 'all',
                link: 'kolokwia/semestr-1/histologia-kolokwia-1.html'
            },
            {
                date: '2025-12-10',
                subject: 'Biochemia',
                type: 'Kolokwium 1',
                topic: 'Chemia, białka, enzymy',
                groups: 'all',
                link: 'kolokwia/semestr-1/biochemia-kolokwia-1.html'
            },
        ];

        // Filter events for user's group and future dates
        return events
            .filter(event => {
                const eventDate = new Date(event.date);
                if (eventDate < today) return false;

                if (event.groups === 'all') return true;
                if (Array.isArray(event.groups)) {
                    return event.groups.includes(parseInt(group));
                }
                return false;
            })
            .sort((a, b) => new Date(a.date) - new Date(b.date))
            .slice(0, 5); // Show max 5 upcoming events
    }

    function getNextWeekClasses(group) {
        // TODO: Load from schedule_data_v2.json
        // For now, return placeholder

        return [
            {
                day: 'Poniedziałek',
                time: '08:00-09:30',
                subject: 'Anatomia',
                type: 'Wykład'
            },
            {
                day: 'Poniedziałek',
                time: '10:00-12:00',
                subject: 'Anatomia',
                type: 'Ćwiczenia'
            },
            {
                day: 'Wtorek',
                time: '13:00-15:00',
                subject: 'Histologia',
                type: 'Ćwiczenia'
            },
        ].slice(0, 10); // Show max 10 classes
    }

    function getDaysUntil(dateString) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const targetDate = new Date(dateString);
        targetDate.setHours(0, 0, 0, 0);

        const diffTime = targetDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        return diffDays;
    }

    function formatDate(dateString) {
        const months = [
            'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
            'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'
        ];

        const date = new Date(dateString);
        const day = date.getDate();
        const month = months[date.getMonth()];
        const year = date.getFullYear();

        return `${day} ${month} ${year}`;
    }

})();
