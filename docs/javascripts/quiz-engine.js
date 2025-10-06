/**
 * CMUJ Wiki - Quiz Engine
 *
 * Interactive quiz system for testing knowledge
 * Features: multiple choice, single choice, explanations, progress tracking
 */

(function() {
    'use strict';

    // ============================================================================
    // CONFIGURATION
    // ============================================================================

    const STORAGE_KEYS = {
        QUIZ_HISTORY: 'cmuj_quiz_history',
        CURRENT_SESSION: 'cmuj_current_quiz_session',
        INSTANT_FEEDBACK: 'cmuj_instant_feedback_enabled'
    };

    // Available quizzes - in production, this would be loaded from JSON
    const AVAILABLE_QUIZZES = [
        {
            id: 'anatomia-osteologia',
            subject: 'Anatomia',
            topic: 'Osteologia',
            difficulty: 'podstawowy',
            semester: 1,
            questionCount: 10,
            description: 'Quiz sprawdzający podstawową wiedzę z osteologii - nauki o kościach.'
        },
        {
            id: 'biochemia-bialka',
            subject: 'Biochemia',
            topic: 'Białka - podstawy',
            difficulty: 'podstawowy',
            semester: 1,
            questionCount: 5,
            description: 'Quiz sprawdzający podstawową wiedzę o budowie i funkcjach białek.'
        }
    ];

    // Hardcoded quiz data (in production, this would be fetched from YAML/JSON)
    const QUIZ_DATA = {
        'anatomia-osteologia': {
            quiz_id: 'anatomia-osteologia',
            subject: 'Anatomia',
            topic: 'Osteologia',
            difficulty: 'podstawowy',
            semester: 1,
            description: 'Quiz sprawdzający podstawową wiedzę z osteologii - nauki o kościach.',
            questions: [
                {
                    id: 'anat-osteo-001',
                    question: 'Ile kości ma dorosły człowiek?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: '206', correct: true },
                        { text: '208', correct: false },
                        { text: '204', correct: false },
                        { text: '210', correct: false }
                    ],
                    explanation: 'Dorosły człowiek ma 206 kości. Noworodek ma ich około 270, ale wiele się zrasta w trakcie rozwoju.'
                },
                {
                    id: 'anat-osteo-002',
                    question: 'Która kość jest najdłuższą kością w ludzkim ciele?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Kość ramieniowa (humerus)', correct: false },
                        { text: 'Kość udowa (femur)', correct: true },
                        { text: 'Kość piszczelowa (tibia)', correct: false },
                        { text: 'Kość promieniowa (radius)', correct: false }
                    ],
                    explanation: 'Kość udowa (femur) to najdłuższa i najsilniejsza kość w ciele człowieka, stanowi około 26% wzrostu człowieka.'
                },
                {
                    id: 'anat-osteo-003',
                    question: 'Zaznacz wszystkie kości długie:',
                    type: 'multiple_choice',
                    points: 2,
                    options: [
                        { text: 'Kość udowa (femur)', correct: true },
                        { text: 'Kość ramieniowa (humerus)', correct: true },
                        { text: 'Łopatka (scapula)', correct: false },
                        { text: 'Kość piszczelowa (tibia)', correct: true },
                        { text: 'Kość potyliczna', correct: false }
                    ],
                    explanation: 'Kości długie to: kość udowa, ramieniowa, piszczelowa, strzałkowa, łokciowa i promieniowa. Łopatka to kość płaska, a kość potyliczna to kość czaszki.'
                },
                {
                    id: 'anat-osteo-004',
                    question: 'Która część kości długiej odpowiada za wzrost kości na długość u dzieci?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Nasada (epifiza)', correct: false },
                        { text: 'Chrząstka nasadowa (płytka wzrostowa)', correct: true },
                        { text: 'Trzon (diafiza)', correct: false },
                        { text: 'Okostna (periosteum)', correct: false }
                    ],
                    explanation: 'Chrząstka nasadowa (płytka wzrostowa) znajduje się pomiędzy nasadą a trzonem kości i odpowiada za wzrost kości na długość do momentu zakończenia wzrostu.'
                },
                {
                    id: 'anat-osteo-005',
                    question: 'Co stanowi około 65-70% masy kości?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Włókna kolagenowe', correct: false },
                        { text: 'Substancje mineralne (głównie fosforany wapnia)', correct: true },
                        { text: 'Komórki kostne (osteocyty)', correct: false },
                        { text: 'Woda', correct: false }
                    ],
                    explanation: 'Substancje mineralne, głównie fosforany wapnia w postaci hydroksyapatytu, stanowią około 65-70% masy kości i zapewniają jej twardość.'
                },
                {
                    id: 'anat-osteo-006',
                    question: 'Zaznacz wszystkie funkcje układu kostnego:',
                    type: 'multiple_choice',
                    points: 2,
                    options: [
                        { text: 'Podpora i kształt ciała', correct: true },
                        { text: 'Ochrona narządów wewnętrznych', correct: true },
                        { text: 'Wytwarzanie krwinek', correct: true },
                        { text: 'Magazynowanie tłuszczu', correct: true },
                        { text: 'Produkcja hormonów płciowych', correct: false }
                    ],
                    explanation: 'Układ kostny pełni wiele funkcji: podporę, ochronę, wytwarzanie krwinek w szpiku czerwonym, magazynowanie minerałów i tłuszczu w szpiku żółtym. Hormony płciowe są produkowane głównie w gonadach.'
                },
                {
                    id: 'anat-osteo-007',
                    question: 'Ile kości czaszki ma dorosły człowiek?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: '22', correct: true },
                        { text: '26', correct: false },
                        { text: '18', correct: false },
                        { text: '20', correct: false }
                    ],
                    explanation: 'Czaszka dorosłego człowieka składa się z 22 kości: 8 kości mózgoczaszki i 14 kości twarzoczaszki.'
                },
                {
                    id: 'anat-osteo-008',
                    question: 'Która z poniższych kości NIE należy do kości nadgarstka?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Kość łódkowata (os scaphoideum)', correct: false },
                        { text: 'Kość półksiężycowata (os lunatum)', correct: false },
                        { text: 'Kość śródręcza (os metacarpale)', correct: true },
                        { text: 'Kość główkowata (os capitatum)', correct: false }
                    ],
                    explanation: 'Kości śródręcza (ossa metacarpalia) tworzą śródręcze, a nie nadgarstek. Nadgarstek składa się z 8 kości ułożonych w dwóch rzędach.'
                },
                {
                    id: 'anat-osteo-009',
                    question: 'Ile kręgów ma kręgosłup człowieka (bez liczenia kości krzyżowej i guzicznej)?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: '24', correct: true },
                        { text: '26', correct: false },
                        { text: '33', correct: false },
                        { text: '30', correct: false }
                    ],
                    explanation: 'Kręgosłup ma 24 wolne kręgi: 7 szyjnych, 12 piersiowych, 5 lędźwiowych. Dodatkowo 5 zrośniętych kręgów krzyżowych i 4-5 zrośniętych kręgów guzicznych.'
                },
                {
                    id: 'anat-osteo-010',
                    question: 'Zaznacz wszystkie elementy żebra:',
                    type: 'multiple_choice',
                    points: 2,
                    options: [
                        { text: 'Główka żebra', correct: true },
                        { text: 'Szyja żebra', correct: true },
                        { text: 'Trzon żebra', correct: true },
                        { text: 'Guzek żebra', correct: true },
                        { text: 'Nasada żebra', correct: false }
                    ],
                    explanation: 'Żebro składa się z: główki (caput), szyi (collum), guzka (tuberculum) i trzonu (corpus). Nie ma nasady - to element kości długich.'
                }
            ]
        },
        'biochemia-bialka': {
            quiz_id: 'biochemia-bialka',
            subject: 'Biochemia',
            topic: 'Białka - podstawy',
            difficulty: 'podstawowy',
            semester: 1,
            description: 'Quiz sprawdzający podstawową wiedzę o budowie i funkcjach białek.',
            questions: [
                {
                    id: 'biochem-prot-001',
                    question: 'Ile różnych aminokwasów białkowych występuje w organizmie człowieka?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: '10', correct: false },
                        { text: '20', correct: true },
                        { text: '30', correct: false },
                        { text: '50', correct: false }
                    ],
                    explanation: 'W organizmie człowieka występuje 20 standardowych aminokwasów białkowych, które są kodowane genetycznie.'
                },
                {
                    id: 'biochem-prot-002',
                    question: 'Które wiązanie łączy aminokwasy w łańcuchu polipeptydowym?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Wiązanie wodorowe', correct: false },
                        { text: 'Wiązanie peptydowe', correct: true },
                        { text: 'Wiązanie disulfidowe', correct: false },
                        { text: 'Wiązanie jonowe', correct: false }
                    ],
                    explanation: 'Wiązanie peptydowe to wiązanie amidowe powstające między grupą karboksylową jednego aminokwasu a grupą aminową drugiego aminokwasu z wydzieleniem cząsteczki wody.'
                },
                {
                    id: 'biochem-prot-003',
                    question: 'Zaznacz wszystkie poziomy struktury białka:',
                    type: 'multiple_choice',
                    points: 2,
                    options: [
                        { text: 'Struktura I-rzędowa (pierwotna)', correct: true },
                        { text: 'Struktura II-rzędowa (wtórna)', correct: true },
                        { text: 'Struktura III-rzędowa (trzeciorzędowa)', correct: true },
                        { text: 'Struktura IV-rzędowa (czwartorzędowa)', correct: true },
                        { text: 'Struktura V-rzędowa', correct: false }
                    ],
                    explanation: 'Białka mają cztery poziomy struktury: I-rzędowa (sekwencja aminokwasów), II-rzędowa (helisa α, kartka β), III-rzędowa (przestrzenna struktura łańcucha), IV-rzędowa (kilka podjednostek).'
                },
                {
                    id: 'biochem-prot-004',
                    question: 'Który aminokwas ma grupę tiolową (-SH) w łańcuchu bocznym?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Seryna', correct: false },
                        { text: 'Cysteina', correct: true },
                        { text: 'Metionina', correct: false },
                        { text: 'Lizyna', correct: false }
                    ],
                    explanation: 'Cysteina ma grupę tiolową (-SH), która może tworzyć mostki disulfidowe z inną cysteiną, stabilizując strukturę białka.'
                },
                {
                    id: 'biochem-prot-005',
                    question: 'Co to jest denaturacja białka?',
                    type: 'single_choice',
                    points: 1,
                    options: [
                        { text: 'Synteza nowego białka', correct: false },
                        { text: 'Utrata struktury przestrzennej bez zerwania wiązań peptydowych', correct: true },
                        { text: 'Rozkład białka na aminokwasy', correct: false },
                        { text: 'Przyłączenie grupy fosforanowej', correct: false }
                    ],
                    explanation: 'Denaturacja to utrata struktury II, III i IV-rzędowej białka pod wpływem czynników fizycznych lub chemicznych, bez zerwania wiązań peptydowych (struktura I-rzędowa pozostaje nienaruszona).'
                }
            ]
        }
    };

    // ============================================================================
    // INITIALIZATION
    // ============================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initQuizSystem);
    } else {
        initQuizSystem();
    }

    // Re-initialize on instant navigation (MkDocs Material)
    document.addEventListener('DOMContentLoaded', function() {
        // Listen for Material's navigation events
        if (typeof document$ !== 'undefined') {
            document$.subscribe(function() {
                initQuizSystem();
            });
        }
    });

    function initQuizSystem() {
        const currentPage = window.location.pathname;

        if (currentPage.includes('testy/index.html') || currentPage.endsWith('testy/')) {
            initQuizBrowser();
        } else if (currentPage.includes('testy/sesja.html')) {
            initQuizSession();
        }
    }

    // ============================================================================
    // QUIZ BROWSER (List Page)
    // ============================================================================

    function initQuizBrowser() {
        const quizListContainer = document.getElementById('quiz-list');
        if (!quizListContainer) return;

        renderQuizList(quizListContainer);
        renderQuizStats();
    }

    function renderQuizList(container) {
        const history = getQuizHistory();

        let html = '';
        AVAILABLE_QUIZZES.forEach(quiz => {
            const attempts = history.filter(h => h.quizId === quiz.id);
            const bestScore = attempts.length > 0
                ? Math.max(...attempts.map(a => a.scorePercent))
                : null;

            html += `
                <div class="quiz-card" data-quiz-id="${quiz.id}">
                    <div class="quiz-card-header">
                        <div class="quiz-subject-badge">${quiz.subject}</div>
                        ${bestScore !== null ? `<div class="quiz-best-score">${Math.round(bestScore)}%</div>` : ''}
                    </div>
                    <h3 class="quiz-card-title">${quiz.topic}</h3>
                    <p class="quiz-card-description">${quiz.description}</p>
                    <div class="quiz-card-meta">
                        <span class="quiz-meta-item">📝 ${quiz.questionCount} pytań</span>
                        <span class="quiz-meta-item">⭐ ${quiz.difficulty}</span>
                        <span class="quiz-meta-item">📚 Semestr ${quiz.semester}</span>
                    </div>
                    ${attempts.length > 0 ? `<div class="quiz-attempts">Rozwiązany ${attempts.length}x</div>` : ''}
                    <button class="quiz-start-btn" onclick="window.quizEngine.startQuiz('${quiz.id}')">
                        ${attempts.length > 0 ? '🔄 Rozwiąż ponownie' : '▶️ Rozpocznij test'}
                    </button>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    function renderQuizStats() {
        const history = getQuizHistory();

        const totalQuizzes = document.getElementById('total-quizzes');
        const avgScore = document.getElementById('avg-score');
        const bestSubject = document.getElementById('best-subject');

        if (totalQuizzes) totalQuizzes.textContent = history.length;

        if (history.length > 0 && avgScore) {
            const avg = history.reduce((sum, h) => sum + h.scorePercent, 0) / history.length;
            avgScore.textContent = Math.round(avg) + '%';
        }

        if (history.length > 0 && bestSubject) {
            const subjectScores = {};
            history.forEach(h => {
                const quiz = AVAILABLE_QUIZZES.find(q => q.id === h.quizId);
                if (quiz) {
                    if (!subjectScores[quiz.subject]) subjectScores[quiz.subject] = [];
                    subjectScores[quiz.subject].push(h.scorePercent);
                }
            });

            let best = null;
            let bestAvg = 0;
            Object.keys(subjectScores).forEach(subject => {
                const avg = subjectScores[subject].reduce((a, b) => a + b, 0) / subjectScores[subject].length;
                if (avg > bestAvg) {
                    bestAvg = avg;
                    best = subject;
                }
            });

            bestSubject.textContent = best || '-';
        }
    }

    // ============================================================================
    // QUIZ SESSION (Active Quiz)
    // ============================================================================

    let currentQuizState = null;

    function initQuizSession() {
        const container = document.getElementById('quiz-session-container');
        if (!container) return;

        // Try to load quiz from URL parameter or localStorage
        const urlParams = new URLSearchParams(window.location.search);
        const quizId = urlParams.get('quiz');

        if (quizId && QUIZ_DATA[quizId]) {
            startQuizSession(quizId);
        } else {
            // Try to resume from localStorage
            const savedSession = localStorage.getItem(STORAGE_KEYS.CURRENT_SESSION);
            if (savedSession) {
                currentQuizState = JSON.parse(savedSession);
                renderQuestion();
            } else {
                container.innerHTML = `
                    <div class="quiz-error">
                        <p>❌ Nie wybrano testu.</p>
                        <p><a href="index.html">Wróć do listy testów</a></p>
                    </div>
                `;
            }
        }
    }

    function startQuizSession(quizId) {
        const quizData = QUIZ_DATA[quizId];
        if (!quizData) {
            console.error('Quiz not found:', quizId);
            return;
        }

        currentQuizState = {
            quizId: quizId,
            quizData: quizData,
            currentQuestionIndex: 0,
            answers: {},
            instantFeedback: getInstantFeedbackEnabled(),
            showingFeedback: false,
            startTime: Date.now()
        };

        saveCurrentSession();
        renderQuestion();
    }

    function renderQuestion() {
        const container = document.getElementById('quiz-session-container');
        if (!container || !currentQuizState) return;

        const { quizData, currentQuestionIndex, answers } = currentQuizState;
        const question = quizData.questions[currentQuestionIndex];
        const totalQuestions = quizData.questions.length;
        const isLastQuestion = currentQuestionIndex === totalQuestions - 1;

        let html = `
            <div class="quiz-session">
                <div class="quiz-header">
                    <div class="quiz-header-top">
                        <h2>${quizData.subject} - ${quizData.topic}</h2>
                        <div class="quiz-settings">
                            <label class="instant-feedback-toggle">
                                <input
                                    type="checkbox"
                                    id="instant-feedback-checkbox"
                                    ${currentQuizState.instantFeedback ? 'checked' : ''}
                                    onchange="window.quizEngine.toggleInstantFeedback(this.checked)"
                                >
                                <span>💡 Natychmiastowa odpowiedź</span>
                            </label>
                        </div>
                    </div>
                    <div class="quiz-progress">
                        <div class="quiz-progress-bar">
                            <div class="quiz-progress-fill" style="width: ${(currentQuestionIndex / totalQuestions) * 100}%"></div>
                        </div>
                        <div class="quiz-progress-text">Pytanie ${currentQuestionIndex + 1} / ${totalQuestions}</div>
                    </div>
                </div>

                <div class="quiz-question-container ${currentQuizState.showingFeedback ? 'showing-feedback' : ''}">
                    <div class="quiz-question-header">
                        <div class="quiz-question-number">Pytanie ${currentQuestionIndex + 1}</div>
                        <div class="quiz-question-points">${question.points} pkt</div>
                    </div>
                    <div class="quiz-question-text">${question.question}</div>

                    <div class="quiz-options">
                        ${renderOptions(question, currentQuestionIndex)}
                    </div>

                    ${currentQuizState.showingFeedback ? renderInstantFeedback(question, currentQuestionIndex) : ''}
                </div>

                <div class="quiz-navigation">
                    ${currentQuestionIndex > 0 && !currentQuizState.showingFeedback ? `
                        <button class="quiz-btn quiz-btn-secondary" onclick="window.quizEngine.previousQuestion()">
                            ← Poprzednie
                        </button>
                    ` : '<div></div>'}

                    ${currentQuizState.showingFeedback ? `
                        ${isLastQuestion ? `
                            <button class="quiz-btn quiz-btn-primary" onclick="window.quizEngine.nextAfterFeedback()">
                                Zobacz wyniki testu →
                            </button>
                        ` : `
                            <button class="quiz-btn quiz-btn-primary" onclick="window.quizEngine.nextAfterFeedback()">
                                Następne pytanie →
                            </button>
                        `}
                    ` : `
                        ${currentQuizState.instantFeedback && answers[currentQuestionIndex] !== undefined ? `
                            <button class="quiz-btn quiz-btn-primary" onclick="window.quizEngine.checkAnswer()">
                                Sprawdź odpowiedź →
                            </button>
                        ` : isLastQuestion ? `
                            <button class="quiz-btn quiz-btn-primary" onclick="window.quizEngine.finishQuiz()">
                                Zakończ test →
                            </button>
                        ` : `
                            <button class="quiz-btn quiz-btn-primary" onclick="window.quizEngine.nextQuestion()">
                                Następne →
                            </button>
                        `}
                    `}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    function renderOptions(question, questionIndex) {
        const userAnswer = currentQuizState.answers[questionIndex];
        const showingFeedback = currentQuizState.showingFeedback;
        let html = '';

        question.options.forEach((option, optionIndex) => {
            const inputType = question.type === 'single_choice' ? 'radio' : 'checkbox';
            const inputName = `question-${questionIndex}`;
            const inputId = `q${questionIndex}-opt${optionIndex}`;

            let isChecked = false;
            if (userAnswer !== undefined) {
                if (question.type === 'single_choice') {
                    isChecked = userAnswer === optionIndex;
                } else {
                    isChecked = Array.isArray(userAnswer) && userAnswer.includes(optionIndex);
                }
            }

            let optionClass = 'quiz-option';
            if (showingFeedback) {
                if (option.correct) {
                    optionClass += ' option-correct';
                } else if (isChecked) {
                    optionClass += ' option-wrong';
                }
            }

            html += `
                <div class="${optionClass}">
                    <input
                        type="${inputType}"
                        id="${inputId}"
                        name="${inputName}"
                        value="${optionIndex}"
                        ${isChecked ? 'checked' : ''}
                        ${showingFeedback ? 'disabled' : ''}
                        onchange="window.quizEngine.selectAnswer(${questionIndex}, ${optionIndex}, '${question.type}')"
                    >
                    <label for="${inputId}">
                        ${showingFeedback && option.correct ? '✓ ' : ''}
                        ${showingFeedback && !option.correct && isChecked ? '✗ ' : ''}
                        ${option.text}
                    </label>
                </div>
            `;
        });

        return html;
    }

    function renderInstantFeedback(question, questionIndex) {
        const userAnswer = currentQuizState.answers[questionIndex];
        const isCorrect = checkIfAnswerCorrect(question, userAnswer);

        return `
            <div class="instant-feedback ${isCorrect ? 'feedback-correct' : 'feedback-incorrect'}">
                <div class="feedback-header">
                    ${isCorrect
                        ? '<span class="feedback-icon">✅</span><strong>Poprawna odpowiedź!</strong>'
                        : '<span class="feedback-icon">❌</span><strong>Niepoprawna odpowiedź</strong>'
                    }
                </div>
                <div class="feedback-explanation">
                    <strong>Wyjaśnienie:</strong> ${question.explanation}
                </div>
                ${isCorrect
                    ? `<div class="feedback-points">+${question.points} pkt</div>`
                    : `<div class="feedback-points">0 pkt</div>`
                }
            </div>
        `;
    }

    function checkIfAnswerCorrect(question, userAnswer) {
        if (userAnswer === undefined) return false;

        if (question.type === 'single_choice') {
            return question.options[userAnswer].correct;
        } else {
            const correctIndices = question.options
                .map((opt, i) => opt.correct ? i : -1)
                .filter(i => i !== -1);
            const userAnswerArray = userAnswer || [];

            return correctIndices.length === userAnswerArray.length &&
                   correctIndices.every(i => userAnswerArray.includes(i));
        }
    }

    function checkAnswer() {
        currentQuizState.showingFeedback = true;
        saveCurrentSession();
        renderQuestion();
        window.scrollTo(0, document.querySelector('.instant-feedback').offsetTop - 100);
    }

    function nextAfterFeedback() {
        currentQuizState.showingFeedback = false;

        if (currentQuizState.currentQuestionIndex < currentQuizState.quizData.questions.length - 1) {
            currentQuizState.currentQuestionIndex++;
            saveCurrentSession();
            renderQuestion();
            window.scrollTo(0, 0);
        } else {
            finishQuiz();
        }
    }

    function toggleInstantFeedback(checked) {
        currentQuizState.instantFeedback = checked;
        localStorage.setItem(STORAGE_KEYS.INSTANT_FEEDBACK, JSON.stringify(checked));
        saveCurrentSession();
    }

    function getInstantFeedbackEnabled() {
        const stored = localStorage.getItem(STORAGE_KEYS.INSTANT_FEEDBACK);
        return stored ? JSON.parse(stored) : false;
    }

    function selectAnswer(questionIndex, optionIndex, questionType) {
        if (questionType === 'single_choice') {
            currentQuizState.answers[questionIndex] = optionIndex;
        } else {
            if (!currentQuizState.answers[questionIndex]) {
                currentQuizState.answers[questionIndex] = [];
            }
            const answerArray = currentQuizState.answers[questionIndex];
            const idx = answerArray.indexOf(optionIndex);
            if (idx > -1) {
                answerArray.splice(idx, 1);
            } else {
                answerArray.push(optionIndex);
            }
        }
        saveCurrentSession();

        // Defer re-render to allow browser to complete input state update
        setTimeout(() => {
            renderQuestion();
        }, 0);
    }

    function nextQuestion() {
        if (currentQuizState.currentQuestionIndex < currentQuizState.quizData.questions.length - 1) {
            currentQuizState.currentQuestionIndex++;
            currentQuizState.showingFeedback = false; // Reset feedback state
            saveCurrentSession();
            renderQuestion();
            window.scrollTo(0, 0);
        }
    }

    function previousQuestion() {
        if (currentQuizState.currentQuestionIndex > 0) {
            currentQuizState.currentQuestionIndex--;
            currentQuizState.showingFeedback = false; // Reset feedback state
            saveCurrentSession();
            renderQuestion();
            window.scrollTo(0, 0);
        }
    }

    function finishQuiz() {
        const result = calculateResults();
        saveQuizResult(result);
        renderResults(result);
        clearCurrentSession();
    }

    function calculateResults() {
        const { quizData, answers, startTime } = currentQuizState;
        let totalPoints = 0;
        let earnedPoints = 0;
        const questionResults = [];

        quizData.questions.forEach((question, index) => {
            totalPoints += question.points;
            const userAnswer = answers[index];
            let correct = false;
            let pointsEarned = 0;

            if (question.type === 'single_choice') {
                correct = userAnswer !== undefined && question.options[userAnswer].correct;
                pointsEarned = correct ? question.points : 0;
            } else {
                const correctIndices = question.options
                    .map((opt, i) => opt.correct ? i : -1)
                    .filter(i => i !== -1);
                const userAnswerArray = userAnswer || [];

                correct = correctIndices.length === userAnswerArray.length &&
                          correctIndices.every(i => userAnswerArray.includes(i));
                pointsEarned = correct ? question.points : 0;
            }

            earnedPoints += pointsEarned;
            questionResults.push({
                question: question,
                userAnswer: userAnswer,
                correct: correct,
                pointsEarned: pointsEarned
            });
        });

        return {
            quizId: currentQuizState.quizId,
            quizData: quizData,
            questionResults: questionResults,
            totalPoints: totalPoints,
            earnedPoints: earnedPoints,
            scorePercent: (earnedPoints / totalPoints) * 100,
            timeSpent: Date.now() - startTime,
            completedAt: new Date().toISOString()
        };
    }

    function renderResults(result) {
        const container = document.getElementById('quiz-session-container');
        if (!container) return;

        const scorePercent = Math.round(result.scorePercent);
        const scoreClass = scorePercent >= 90 ? 'excellent' :
                          scorePercent >= 75 ? 'good' :
                          scorePercent >= 50 ? 'pass' : 'fail';

        let html = `
            <div class="quiz-results">
                <div class="quiz-results-header">
                    <h2>🎯 Wyniki testu</h2>
                    <div class="quiz-subject-info">${result.quizData.subject} - ${result.quizData.topic}</div>
                </div>

                <div class="quiz-score-panel ${scoreClass}">
                    <div class="quiz-score-main">
                        <div class="quiz-score-number">${scorePercent}%</div>
                        <div class="quiz-score-label">${result.earnedPoints} / ${result.totalPoints} punktów</div>
                    </div>
                    <div class="quiz-score-message">
                        ${getScoreMessage(scorePercent)}
                    </div>
                </div>

                <div class="quiz-results-summary">
                    <div class="summary-stat">
                        <div class="stat-icon">✅</div>
                        <div class="stat-value">${result.questionResults.filter(r => r.correct).length}</div>
                        <div class="stat-label">Poprawne</div>
                    </div>
                    <div class="summary-stat">
                        <div class="stat-icon">❌</div>
                        <div class="stat-value">${result.questionResults.filter(r => !r.correct).length}</div>
                        <div class="stat-label">Błędne</div>
                    </div>
                    <div class="summary-stat">
                        <div class="stat-icon">⏱️</div>
                        <div class="stat-value">${formatTime(result.timeSpent)}</div>
                        <div class="stat-label">Czas</div>
                    </div>
                </div>

                <div class="quiz-review-section">
                    <h3>📋 Przegląd odpowiedzi</h3>
                    ${renderReview(result)}
                </div>

                <div class="quiz-actions">
                    <a href="index.html" class="quiz-btn quiz-btn-secondary">← Wróć do listy testów</a>
                    <button class="quiz-btn quiz-btn-primary" onclick="window.quizEngine.startQuiz('${result.quizId}')">
                        🔄 Rozwiąż ponownie
                    </button>
                </div>
            </div>
        `;

        container.innerHTML = html;
        window.scrollTo(0, 0);
    }

    function renderReview(result) {
        let html = '';

        result.questionResults.forEach((qr, index) => {
            const question = qr.question;
            const statusIcon = qr.correct ? '✅' : '❌';
            const statusClass = qr.correct ? 'correct' : 'incorrect';

            html += `
                <div class="review-question ${statusClass}">
                    <div class="review-question-header">
                        <span class="review-status">${statusIcon}</span>
                        <span class="review-number">Pytanie ${index + 1}</span>
                        <span class="review-points">${qr.pointsEarned} / ${question.points} pkt</span>
                    </div>
                    <div class="review-question-text">${question.question}</div>
                    <div class="review-options">
                        ${renderReviewOptions(question, qr.userAnswer)}
                    </div>
                    <div class="review-explanation">
                        <strong>Wyjaśnienie:</strong> ${question.explanation}
                    </div>
                </div>
            `;
        });

        return html;
    }

    function renderReviewOptions(question, userAnswer) {
        let html = '';

        question.options.forEach((option, index) => {
            const isCorrect = option.correct;
            const isUserAnswer = question.type === 'single_choice'
                ? userAnswer === index
                : (userAnswer || []).includes(index);

            let optionClass = '';
            if (isCorrect) optionClass = 'option-correct';
            if (isUserAnswer && !isCorrect) optionClass = 'option-wrong';

            let icon = '';
            if (isCorrect) icon = '✓';
            if (isUserAnswer && !isCorrect) icon = '✗';
            if (isUserAnswer && isCorrect) icon = '✓';

            html += `
                <div class="review-option ${optionClass}">
                    <span class="review-option-icon">${icon}</span>
                    <span class="review-option-text">${option.text}</span>
                    ${isUserAnswer ? '<span class="review-option-badge">Twoja odpowiedź</span>' : ''}
                </div>
            `;
        });

        return html;
    }

    function getScoreMessage(scorePercent) {
        if (scorePercent >= 90) return '🌟 Świetna robota! Doskonały wynik!';
        if (scorePercent >= 75) return '👍 Bardzo dobrze! Solidna wiedza!';
        if (scorePercent >= 50) return '📚 Niezłe! Ale jest jeszcze przestrzeń na poprawę.';
        return '💪 Nie poddawaj się! Przećwicz materiał i spróbuj ponownie.';
    }

    function formatTime(milliseconds) {
        const seconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;

        if (minutes > 0) {
            return `${minutes}m ${remainingSeconds}s`;
        }
        return `${seconds}s`;
    }

    // ============================================================================
    // LOCAL STORAGE
    // ============================================================================

    function getQuizHistory() {
        const stored = localStorage.getItem(STORAGE_KEYS.QUIZ_HISTORY);
        return stored ? JSON.parse(stored) : [];
    }

    function saveQuizResult(result) {
        const history = getQuizHistory();
        history.push({
            quizId: result.quizId,
            scorePercent: result.scorePercent,
            earnedPoints: result.earnedPoints,
            totalPoints: result.totalPoints,
            completedAt: result.completedAt,
            timeSpent: result.timeSpent
        });
        localStorage.setItem(STORAGE_KEYS.QUIZ_HISTORY, JSON.stringify(history));
    }

    function saveCurrentSession() {
        localStorage.setItem(STORAGE_KEYS.CURRENT_SESSION, JSON.stringify(currentQuizState));
    }

    function clearCurrentSession() {
        localStorage.removeItem(STORAGE_KEYS.CURRENT_SESSION);
    }

    // ============================================================================
    // PUBLIC API
    // ============================================================================

    window.quizEngine = {
        startQuiz: function(quizId) {
            window.location.href = `sesja.html?quiz=${quizId}`;
        },
        selectAnswer: selectAnswer,
        nextQuestion: nextQuestion,
        previousQuestion: previousQuestion,
        finishQuiz: finishQuiz,
        checkAnswer: checkAnswer,
        nextAfterFeedback: nextAfterFeedback,
        toggleInstantFeedback: toggleInstantFeedback
    };

})();
