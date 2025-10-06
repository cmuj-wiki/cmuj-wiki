/**
 * CMUJ Wiki - Calendar Widget (BETA)
 *
 * Interactive weekly calendar for class schedule
 * Features: data normalization, conflict detection, debugging tools
 */

(function() {
    'use strict';

    // ============================================================================
    // CONFIGURATION
    // ============================================================================

    const STORAGE_KEY = 'cmuj_user_group';
    const SCHEDULE_DATA_URL = '../static/schedule_data_v2.json';
    const HOLIDAYS_DATA_URL = '../static/holidays.json';

    // Calendar configuration
    const WEEK_DAYS = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'];
    const START_HOUR = 8;
    const END_HOUR = 19;
    const SLOT_MINUTES = 15;
    const DEFAULT_DURATION = 90; // minutes (fallback when duration not in data)

    // Dynamic row height based on view mode
    const ROW_HEIGHT_NORMAL = 20;  // px - compact for fitting on page
    const ROW_HEIGHT_FULLSCREEN = 35;  // px - comfortable for reading hours

    // Academic year bounds (winter semester 2024/2025)
    // Note: Extended to handle system date variations and allow browsing full year
    const SEMESTER_START = new Date(2024, 9, 2); // Oct 2, 2024 (month is 0-indexed)
    const SEMESTER_END = new Date(2026, 0, 1);   // Jan 1, 2026 (extended to allow viewing past semester)

    // State
    let scheduleData = null;
    let holidaysData = null;  // Academic calendar: holidays, exam sessions, free days
    let userGroup = null;
    let currentWeekOffset = 0; // 0 = current week, -1 = last week, 1 = next week
    let isFullscreen = false;
    let dataQualityStats = {
        normalized: 0,
        conflicts: 0,
        missingLocation: 0,
        total: 0
    };

    // ============================================================================
    // INITIALIZATION
    // ============================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCalendar);
    } else {
        initCalendar();
    }

    // Re-initialize on instant navigation (MkDocs Material)
    document.addEventListener('DOMContentLoaded', function() {
        if (typeof document$ !== 'undefined') {
            document$.subscribe(function() {
                initCalendar();
            });
        }
    });

    function initCalendar() {
        const container = document.getElementById('calendar-container');
        if (!container) return;

        userGroup = getUserGroup();

        if (!userGroup) {
            renderGroupSelector(container);
        } else {
            loadScheduleData(container);
        }
    }

    // ============================================================================
    // DATA LOADING
    // ============================================================================

    async function loadScheduleData(container) {
        try {
            container.innerHTML = '<div class="calendar-loading">⏳ Ładowanie danych planu...</div>';

            // Load both schedule and holidays in parallel
            const [scheduleResponse, holidaysResponse] = await Promise.all([
                fetch(SCHEDULE_DATA_URL),
                fetch(HOLIDAYS_DATA_URL)
            ]);

            if (!scheduleResponse.ok) throw new Error('Failed to load schedule data');

            scheduleData = await scheduleResponse.json();

            // Holidays are optional (won't break if missing)
            if (holidaysResponse.ok) {
                holidaysData = await holidaysResponse.json();
                console.log(`📅 Loaded ${holidaysData.length} holidays/exam sessions`);
            } else {
                console.warn('⚠️ Could not load holidays.json - calendar will show all events');
                holidaysData = [];
            }

            renderCalendar(container);
        } catch (error) {
            console.error('Error loading schedule:', error);
            container.innerHTML = `
                <div class="calendar-error">
                    <p>❌ Nie udało się załadować danych planu zajęć</p>
                    <p><a href="../plan-zajec.html">Zobacz alternatywny plan →</a></p>
                </div>
            `;
        }
    }

    // ============================================================================
    // GROUP SELECTION
    // ============================================================================

    function getUserGroup() {
        return localStorage.getItem(STORAGE_KEY);
    }

    function setUserGroup(group) {
        localStorage.setItem(STORAGE_KEY, group);
    }

    function renderGroupSelector(container) {
        container.innerHTML = `
            <div class="calendar-group-selector">
                <h3>👋 Wybierz swoją grupę</h3>
                <p>Aby zobaczyć kalendarz, wybierz swoją grupę zajęciową:</p>

                <div class="group-grid">
                    ${Array.from({length: 20}, (_, i) => i + 1).map(num => `
                        <button class="group-btn" data-group="${num}">
                            Grupa ${num}
                        </button>
                    `).join('')}
                </div>

                <p class="calendar-note">
                    💡 Twój wybór zostanie zapamiętany
                </p>
            </div>
        `;

        // Attach listeners
        container.querySelectorAll('.group-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const group = this.dataset.group;
                setUserGroup(group);
                userGroup = group;
                loadScheduleData(container);
            });
        });
    }

    // ============================================================================
    // DATA PROCESSING
    // ============================================================================

    function normalizeEvent(event) {
        const normalized = {...event};
        let hasIssues = false;

        // NOTE: Minute validation is now done in parse_schedule_v2.py
        // All minutes are guaranteed to be 0, 15, 30, or 45

        // Validate data integrity (should never happen with validated parsers)
        if (![0, 15, 30, 45].includes(normalized.minute)) {
            console.error(`Invalid minute value detected: ${normalized.minute} for event:`, event);
            normalized._normalized = true;
            normalized._originalMinute = normalized.minute;
            normalized.minute = Math.round(normalized.minute / 15) * 15;
            hasIssues = true;
        }

        // Default null minute to :00 (legacy data compatibility)
        if (normalized.minute === null) {
            normalized.minute = 0;
        }

        // Use duration from data (detected from merged cells), fallback to default
        if (!normalized.duration || normalized.duration <= 0) {
            normalized.duration = DEFAULT_DURATION;
        }

        // Track missing location
        if (!normalized.location) {
            normalized._missingLocation = true;
        }

        return {event: normalized, hasIssues};
    }

    function filterEventsForGroup(events, group) {
        return events.filter(e => e.group === parseInt(group));
    }

    function detectConflicts(events) {
        const conflicts = [];

        for (let i = 0; i < events.length; i++) {
            for (let j = i + 1; j < events.length; j++) {
                const e1 = events[i];
                const e2 = events[j];

                // Same day and time overlap
                if (e1.day === e2.day && eventsOverlap(e1, e2)) {
                    e1._hasConflict = true;
                    e2._hasConflict = true;
                    conflicts.push([e1, e2]);
                }
            }
        }

        return conflicts;
    }

    function eventsOverlap(e1, e2) {
        const start1 = e1.hour * 60 + e1.minute;
        const end1 = start1 + e1.duration;
        const start2 = e2.hour * 60 + e2.minute;
        const end2 = start2 + e2.duration;

        return (start1 < end2 && start2 < end1);
    }

    // ============================================================================
    // ACADEMIC CALENDAR FILTERING
    // ============================================================================

    function isClassDay(date) {
        /**
         * Checks if the given date is a regular class day.
         * Returns false for holidays, exam sessions, and free days.
         */

        if (!holidaysData || holidaysData.length === 0) {
            return true; // If no holidays data, assume all days have classes
        }

        const dateStr = date.toISOString().split('T')[0]; // YYYY-MM-DD format

        // Check if this date is in holidays/free days
        for (const item of holidaysData) {
            if (item.date === dateStr) {
                // Don't show classes on holidays, exam sessions, or free days
                if (item.type === 'holiday' || item.type === 'exam_session' || item.type === 'free_day') {
                    return false;
                }
            }
        }

        return true;
    }

    function parseRomanMonth(roman) {
        const months = {
            'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5,
            'VII': 6, 'VIII': 7, 'IX': 8, 'X': 9, 'XI': 10, 'XII': 11
        };
        return months[roman] !== undefined ? months[roman] : null;
    }

    function eventActiveInWeek(event, eventDate) {
        /**
         * Checks if event should be shown on the given date.
         * Parses event.dates for restrictions like "do 7.XI" or "28.XI - 16.I"
         *
         * CRITICAL: Year interpretation is based on the eventDate being viewed,
         * not hardcoded, to support viewing multiple academic years.
         */

        if (!event.dates || event.dates.length === 0) {
            return true; // No date restrictions
        }

        // Determine the academic year from the eventDate being viewed
        // Academic year runs Oct-Sep (e.g., 2024-2025 = Oct 2024 to Sep 2025)
        const viewMonth = eventDate.getMonth(); // 0-11
        const viewYear = eventDate.getFullYear();
        const baseYear = viewMonth >= 9 ? viewYear : viewYear - 1; // Sept (8) is end, Oct (9) is start

        // Parse first date restriction (usually only one)
        const dateStr = event.dates[0];

        // Pattern: "do 7.XI" → ends on Nov 7
        const endPattern = /do\s+(\d{1,2})\.([IVX]+)/;
        const endMatch = dateStr.match(endPattern);
        if (endMatch) {
            const day = parseInt(endMatch[1]);
            const month = parseRomanMonth(endMatch[2]);
            if (month !== null) {
                // Oct-Dec = baseYear, Jan-Sep = baseYear+1
                const year = month >= 9 ? baseYear : baseYear + 1;
                const endDate = new Date(year, month, day);
                // CRITICAL: Make endDate INCLUSIVE of the entire day
                // Without this, a class at 10:45 on Nov 7 would be AFTER Nov 7 00:00:00
                endDate.setHours(23, 59, 59, 999);
                // Event runs from semester start until endDate (inclusive)
                return eventDate <= endDate;
            }
        }

        // Pattern: "28.XI - 16.I" → Nov 28 to Jan 16
        const rangePattern = /(\d{1,2})\.([IVX]+)\s*-\s*(\d{1,2})\.([IVX]+)/;
        const rangeMatch = dateStr.match(rangePattern);
        if (rangeMatch) {
            const day1 = parseInt(rangeMatch[1]);
            const month1 = parseRomanMonth(rangeMatch[2]);
            const day2 = parseInt(rangeMatch[3]);
            const month2 = parseRomanMonth(rangeMatch[4]);

            if (month1 !== null && month2 !== null) {
                // Oct-Dec = baseYear, Jan-Sep = baseYear+1
                const year1 = month1 >= 9 ? baseYear : baseYear + 1;
                const year2 = month2 >= month1 ? year1 : year1 + 1;

                const startDate = new Date(year1, month1, day1);
                const endDate = new Date(year2, month2, day2);
                // CRITICAL: Make endDate INCLUSIVE of the entire day
                // A class on Jan 16 at 08:15 should still show (it's the last day)
                endDate.setHours(23, 59, 59, 999);

                return eventDate >= startDate && eventDate <= endDate;
            }
        }

        // If we can't parse the date, show the event (better to show too much than too little)
        return true;
    }

    function filterEventsByWeek(events, weekOffset) {
        /**
         * Filters events to only show those that:
         * 1. Fall within the academic year (Oct 2024 - Jul 2025)
         * 2. Are on days that have classes (not holidays/exam sessions)
         * 3. Respect event-specific date ranges (e.g. "do 7.XI", "28.XI - 16.I")
         */

        const weekInfo = getWeekInfo(weekOffset);
        const monday = weekInfo.monday;

        return events.filter(event => {
            // Calculate the actual date for this event in the selected week
            const eventDate = new Date(monday);
            eventDate.setDate(monday.getDate() + event.day); // day 0 = Monday, 1 = Tuesday, etc.

            // 1. Check if date is within academic year
            if (eventDate < SEMESTER_START || eventDate > SEMESTER_END) {
                return false; // Outside semester bounds
            }

            // 2. Check if this date has classes (not holiday/exam session)
            if (!isClassDay(eventDate)) {
                return false;
            }

            // 3. Check if event is active on this specific date (respects "do 7.XI" etc.)
            if (!eventActiveInWeek(event, eventDate)) {
                return false;
            }

            return true;
        });
    }

    // ============================================================================
    // CALENDAR RENDERING
    // ============================================================================

    function renderCalendar(container) {
        // Get and normalize events for user's group
        let groupEvents = filterEventsForGroup(scheduleData, userGroup);

        // Filter by current week (only show events on class days)
        groupEvents = filterEventsByWeek(groupEvents, currentWeekOffset);

        // Normalize events and track issues
        dataQualityStats = {
            normalized: 0,
            conflicts: 0,
            missingLocation: 0,
            total: groupEvents.length
        };

        groupEvents = groupEvents.map(e => {
            const {event, hasIssues} = normalizeEvent(e);
            if (hasIssues) dataQualityStats.normalized++;
            if (!event.location) dataQualityStats.missingLocation++;
            return event;
        });

        // Detect conflicts
        const conflicts = detectConflicts(groupEvents);
        dataQualityStats.conflicts = conflicts.length;

        // Get current week info
        const weekInfo = getWeekInfo(currentWeekOffset);

        // Render
        const html = `
            <div class="calendar-wrapper ${isFullscreen ? 'calendar-fullscreen' : ''}">
                <div class="calendar-header">
                    <div class="calendar-header-top">
                        <h3>📅 Grupa ${userGroup}</h3>
                        <div class="calendar-header-actions">
                            <button class="calendar-fullscreen-btn" onclick="window.calendar.toggleFullscreen()">
                                ${isFullscreen ? '🗙 Zamknij pełny ekran' : '⛶ Pełny ekran'}
                            </button>
                            <button class="calendar-change-group" onclick="window.calendar.changeGroup()">
                                Zmień grupę
                            </button>
                        </div>
                    </div>

                    <div class="calendar-week-nav">
                        <button class="calendar-nav-btn" onclick="window.calendar.previousWeek()">
                            ← Poprzedni
                        </button>
                        <div class="calendar-week-info">
                            ${weekInfo.label}
                            <br>
                            <small style="opacity: 0.7">${weekInfo.dateRange}</small>
                        </div>
                        <button class="calendar-nav-btn" onclick="window.calendar.nextWeek()">
                            Następny →
                        </button>
                        ${currentWeekOffset !== 0 ? `
                            <button class="calendar-nav-btn" onclick="window.calendar.goToCurrentWeek()">
                                📅 Bieżący tydzień
                            </button>
                        ` : ''}
                    </div>
                </div>

                <div class="calendar-week-view">
                    ${groupEvents.length > 0
                        ? renderWeekGrid(groupEvents)
                        : `<div class="calendar-empty-week">
                            <p>📭 Brak zajęć w tym tygodniu</p>
                            <p><small>Spróbuj nawigować do tygodnia z semestru zimowego (październik 2024 - styczeń 2025) lub letniego (luty - czerwiec 2025)</small></p>
                            <button class="calendar-nav-btn" onclick="window.calendar.goToSemesterStart()">
                                🎓 Przejdź do początku semestru
                            </button>
                          </div>`
                    }
                </div>
            </div>
        `;

        container.innerHTML = html;

        // Render data quality stats
        renderDataQualityStats();
    }

    function renderWeekGrid(events) {
        const totalSlots = (END_HOUR - START_HOUR) * (60 / SLOT_MINUTES);
        const rowHeight = getCurrentRowHeight();

        let html = `<div class="calendar-grid" style="grid-auto-rows: ${rowHeight}px;">`;

        // Header row
        html += '<div class="calendar-time-header"></div>'; // Empty corner
        WEEK_DAYS.forEach(day => {
            html += `<div class="calendar-day-header">${day}</div>`;
        });

        // Time slots and events
        for (let slotIndex = 0; slotIndex < totalSlots; slotIndex++) {
            const slotHour = START_HOUR + Math.floor(slotIndex / 4);
            const slotMinute = (slotIndex % 4) * SLOT_MINUTES;

            // Time label (only on the hour)
            if (slotMinute === 0) {
                html += `<div class="calendar-time-label">${slotHour}:00</div>`;
            } else {
                html += '<div class="calendar-time-label"></div>';
            }

            // Day cells
            for (let dayIndex = 0; dayIndex < 5; dayIndex++) {
                html += `<div class="calendar-cell" data-day="${dayIndex}" data-slot="${slotIndex}">`;

                // Find events that start in this slot
                const cellEvents = events.filter(e => {
                    if (e.day !== dayIndex) return false;

                    const eventSlot = ((e.hour - START_HOUR) * 4) + (e.minute / SLOT_MINUTES);
                    return eventSlot === slotIndex;
                });

                cellEvents.forEach(event => {
                    html += renderEvent(event);
                });

                html += '</div>';
            }
        }

        html += '</div>';
        return html;
    }

    // Helper to get current row height based on view mode
    function getCurrentRowHeight() {
        return isFullscreen ? ROW_HEIGHT_FULLSCREEN : ROW_HEIGHT_NORMAL;
    }

    function renderEvent(event) {
        const durationSlots = Math.ceil(event.duration / SLOT_MINUTES);
        const rowHeight = getCurrentRowHeight();

        let classes = ['calendar-event'];
        if (event._normalized) classes.push('event-normalized');
        if (event._hasConflict) classes.push('event-conflict');
        if (event._missingLocation) classes.push('event-missing-location');

        // Color by subject (hash subject name to hue)
        const hue = hashString(event.subject) % 360;
        const color = `hsl(${hue}, 60%, 85%)`;
        const borderColor = `hsl(${hue}, 60%, 60%)`;

        const time = formatTime(event.hour, event.minute);

        // Calculate end time properly (handle hour overflow)
        const totalMinutes = event.hour * 60 + event.minute + event.duration;
        const endHour = Math.floor(totalMinutes / 60);
        const endMinute = totalMinutes % 60;
        const endTime = formatTime(endHour, endMinute);

        let badges = '';
        if (event._normalized) badges += '<span class="event-badge badge-warning" title="Czas znormalizowany">⚠️</span>';
        if (event._hasConflict) badges += '<span class="event-badge badge-conflict" title="Konflikt">🚨</span>';
        if (event._missingLocation) badges += '<span class="event-badge badge-location" title="Brak lokalizacji">📍</span>';

        return `
            <div class="calendar-event-wrapper" style="height: ${durationSlots * rowHeight}px;">
                <div class="${classes.join(' ')}"
                     style="background: ${color}; border-left: 4px solid ${borderColor};"
                     onclick="window.calendar.showEventDetails(${JSON.stringify(event).replace(/"/g, '&quot;')})">
                    <div class="event-badges">${badges}</div>
                    <div class="event-subject">${event.subject}</div>
                    <div class="event-time">${time} - ${endTime}</div>
                    ${event.location ? `<div class="event-location">${event.location}</div>` : ''}
                    ${event.type ? `<div class="event-type">${event.type}</div>` : ''}
                </div>
            </div>
        `;
    }

    function renderDataQualityStats() {
        const panel = document.getElementById('data-quality-panel');
        if (!panel) return;

        // Handle case when no events in week (avoid NaN)
        let qualityScore = 100;
        if (dataQualityStats.total > 0) {
            qualityScore = Math.round(
                ((dataQualityStats.total - dataQualityStats.normalized - dataQualityStats.conflicts) /
                dataQualityStats.total) * 100
            );
        }

        let statusIcon = '✅';
        let statusClass = 'quality-good';

        // Special case for empty week
        if (dataQualityStats.total === 0) {
            statusIcon = '📭';
            statusClass = 'quality-info';
        } else if (qualityScore < 50) {
            statusIcon = '🚨';
            statusClass = 'quality-poor';
        } else if (qualityScore < 80) {
            statusIcon = '⚠️';
            statusClass = 'quality-fair';
        }

        panel.innerHTML = `
            <div class="quality-card quality-header ${statusClass}">
                <div class="quality-icon">${statusIcon}</div>
                <div class="quality-text">
                    <div class="quality-score">${qualityScore}%</div>
                    <div class="quality-label">Jakość danych</div>
                </div>
            </div>

            <div class="quality-card">
                <div class="quality-stat-value">${dataQualityStats.total}</div>
                <div class="quality-stat-label">Zajęć w tygodniu</div>
            </div>

            <div class="quality-card ${dataQualityStats.normalized > 0 ? 'quality-warning' : ''}">
                <div class="quality-stat-value">${dataQualityStats.normalized}</div>
                <div class="quality-stat-label">Znormalizowane godziny</div>
            </div>

            <div class="quality-card ${dataQualityStats.conflicts > 0 ? 'quality-error' : ''}">
                <div class="quality-stat-value">${dataQualityStats.conflicts}</div>
                <div class="quality-stat-label">Konflikty wykryte</div>
            </div>

            <div class="quality-card ${dataQualityStats.missingLocation > 0 ? 'quality-info' : ''}">
                <div class="quality-stat-value">${dataQualityStats.missingLocation}</div>
                <div class="quality-stat-label">Brak lokalizacji</div>
            </div>
        `;
    }

    // ============================================================================
    // UTILITIES
    // ============================================================================

    function formatTime(hour, minute) {
        const h = hour.toString().padStart(2, '0');
        const m = minute.toString().padStart(2, '0');
        return `${h}:${m}`;
    }

    function hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash);
    }

    function getWeekInfo(weekOffset) {
        const today = new Date();
        const currentDay = today.getDay(); // 0 = Sunday, 1 = Monday, etc.

        // Get Monday of current week
        const monday = new Date(today);
        const daysSinceMonday = currentDay === 0 ? 6 : currentDay - 1; // Adjust for Sunday = 0
        monday.setDate(today.getDate() - daysSinceMonday);

        // Apply offset
        monday.setDate(monday.getDate() + (weekOffset * 7));

        // Get Friday
        const friday = new Date(monday);
        friday.setDate(monday.getDate() + 4);

        // Format dates
        const formatDate = (date) => {
            const day = date.getDate();
            const month = date.getMonth() + 1;
            return `${day}.${month < 10 ? '0' + month : month}`;
        };

        let label;
        if (weekOffset === 0) {
            label = 'Bieżący tydzień';
        } else if (weekOffset === -1) {
            label = 'Poprzedni tydzień';
        } else if (weekOffset === 1) {
            label = 'Następny tydzień';
        } else if (weekOffset < 0) {
            label = `${Math.abs(weekOffset)} tygodnie wstecz`;
        } else {
            label = `Za ${weekOffset} tygodnie`;
        }

        const dateRange = `${formatDate(monday)} - ${formatDate(friday)}`;

        return { label, dateRange, monday, friday };
    }

    // ============================================================================
    // NAVIGATION FUNCTIONS
    // ============================================================================

    function previousWeek() {
        currentWeekOffset--;
        const container = document.getElementById('calendar-container');
        if (container && scheduleData) {
            renderCalendar(container);
        }
    }

    function nextWeek() {
        currentWeekOffset++;
        const container = document.getElementById('calendar-container');
        if (container && scheduleData) {
            renderCalendar(container);
        }
    }

    function goToCurrentWeek() {
        currentWeekOffset = 0;
        const container = document.getElementById('calendar-container');
        if (container && scheduleData) {
            renderCalendar(container);
        }
    }

    function toggleFullscreen() {
        isFullscreen = !isFullscreen;

        // Toggle body scroll
        if (isFullscreen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }

        // Re-render calendar with fullscreen class
        const container = document.getElementById('calendar-container');
        if (container && scheduleData) {
            renderCalendar(container);
        }
    }

    // ============================================================================
    // EVENT DETAILS MODAL
    // ============================================================================

    function showEventDetails(event) {
        const modal = document.createElement('div');
        modal.className = 'event-modal-overlay';
        modal.onclick = function(e) {
            if (e.target === modal) closeModal();
        };

        let debugInfo = '';
        if (event._normalized) {
            debugInfo += `<p class="debug-warning">⚠️ Czas znormalizowany: ${event._originalMinute} → ${event.minute} minut</p>`;
        }
        if (event._hasConflict) {
            debugInfo += `<p class="debug-error">🚨 Wykryto konflikt z innym zajęciem</p>`;
        }

        modal.innerHTML = `
            <div class="event-modal">
                <div class="event-modal-header">
                    <h3>${event.subject}</h3>
                    <button class="event-modal-close" onclick="window.calendar.closeModal()">✕</button>
                </div>
                <div class="event-modal-body">
                    <p><strong>Godzina:</strong> ${formatTime(event.hour, event.minute)} - ${formatTime(Math.floor((event.hour * 60 + event.minute + event.duration) / 60), (event.hour * 60 + event.minute + event.duration) % 60)}</p>
                    <p><strong>Dzień:</strong> ${WEEK_DAYS[event.day]}</p>
                    ${event.location ? `<p><strong>Lokalizacja:</strong> ${event.location}</p>` : '<p><strong>Lokalizacja:</strong> <em>Nie podano</em></p>'}
                    ${event.type ? `<p><strong>Typ:</strong> ${event.type}</p>` : ''}
                    ${event.dates && event.dates.length > 0 ? `<p><strong>Daty:</strong> ${event.dates.join(', ')}</p>` : ''}

                    ${debugInfo}

                    <details class="event-raw-data">
                        <summary>📋 Surowe dane JSON</summary>
                        <pre>${JSON.stringify(event, null, 2)}</pre>
                    </details>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }

    function closeModal() {
        const modal = document.querySelector('.event-modal-overlay');
        if (modal) modal.remove();
    }

    function changeGroup() {
        localStorage.removeItem(STORAGE_KEY);
        userGroup = null;
        const container = document.getElementById('calendar-container');
        if (container) {
            renderGroupSelector(container);
        }
    }

    function goToSemesterStart() {
        // Calculate weeks between now and semester start (Oct 2, 2024)
        const today = new Date();
        const semesterStart = new Date(2024, 9, 2); // Oct 2, 2024

        const diffTime = semesterStart - today;
        const diffWeeks = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 7));

        currentWeekOffset = diffWeeks;
        const container = document.getElementById('calendar-container');
        if (container && scheduleData) {
            renderCalendar(container);
        }
    }

    // ============================================================================
    // PUBLIC API
    // ============================================================================

    window.calendar = {
        changeGroup: changeGroup,
        showEventDetails: showEventDetails,
        closeModal: closeModal,
        previousWeek: previousWeek,
        nextWeek: nextWeek,
        goToCurrentWeek: goToCurrentWeek,
        goToSemesterStart: goToSemesterStart,
        toggleFullscreen: toggleFullscreen
    };

})();
