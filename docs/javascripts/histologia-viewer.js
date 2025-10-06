/**
 * CMUJ Wiki - Histologia Practice Exam Viewer
 * Interactive image-by-image viewer for microscope slides
 */

(function() {
  'use strict';

  class HistologiaViewer {
    constructor(container) {
      this.container = container;
      this.zestaw = container.dataset.zestaw;
      this.currentSlide = 1;
      this.totalSlides = 15;
      this.answersData = null;
      this.answerRevealed = false;

      this.init();
    }

    async init() {
      try {
        // Load answers data - use relative path from docs root
        const response = await fetch('../assets/data/histologia-answers.json');
        this.answersData = await response.json();

        this.render();
      } catch (error) {
        console.error('Error loading histologia answers:', error);
        this.container.innerHTML = `
          <div class="quiz-error">
            <p><strong>Błąd ładowania danych</strong></p>
            <p>Nie udało się załadować odpowiedzi do egzaminu.</p>
          </div>
        `;
      }
    }

    getStoł(slideNumber) {
      if (slideNumber >= 1 && slideNumber <= 5) return 1;
      if (slideNumber >= 6 && slideNumber <= 10) return 2;
      if (slideNumber >= 11 && slideNumber <= 15) return 3;
      return 1;
    }

    render() {
      const stoł = this.getStoł(this.currentSlide);
      const imagePath = `../assets/images/histologia/probny-egzamin/zestaw-${this.zestaw}/${this.currentSlide}.jpg`;
      const answer = this.answersData?.[this.zestaw]?.[this.currentSlide.toString()] || 'Brak odpowiedzi';

      this.container.innerHTML = `
        <div class="histologia-viewer">
          <!-- Header -->
          <div class="quiz-header">
            <div class="histologia-header-top">
              <h3 style="margin: 0;">Zestaw ${this.zestaw} - Stół ${stoł}</h3>
              <div class="histologia-progress-badge">
                ${this.currentSlide}/15
              </div>
            </div>
            <div class="quiz-progress">
              <div class="quiz-progress-bar">
                <div class="quiz-progress-fill" style="width: ${(this.currentSlide / this.totalSlides) * 100}%"></div>
              </div>
            </div>
          </div>

          <!-- Image Container -->
          <div class="histologia-image-container">
            <img
              src="${imagePath}"
              alt="Preparat histologiczny ${this.currentSlide}"
              class="histologia-slide-image"
              onclick="this.classList.toggle('zoomed')"
            />
            <div class="histologia-zoom-hint">💡 Kliknij obraz, aby powiększyć</div>
          </div>

          <!-- Answer Section -->
          <div class="histologia-answer-section ${this.answerRevealed ? 'revealed' : ''}">
            ${this.answerRevealed ? `
              <div class="histologia-answer-box">
                <div class="answer-header">
                  <span class="answer-icon">✓</span>
                  <strong>Odpowiedź:</strong>
                </div>
                <div class="answer-text">${answer}</div>
              </div>
            ` : `
              <button class="quiz-btn quiz-btn-primary" onclick="window.histologiaRevealAnswer()">
                🔍 Pokaż odpowiedź
              </button>
            `}
          </div>

          <!-- Navigation -->
          <div class="quiz-navigation">
            <button
              class="quiz-btn quiz-btn-secondary"
              onclick="window.histologiaPrevSlide()"
              ${this.currentSlide === 1 ? 'disabled' : ''}
            >
              ← Poprzedni preparat
            </button>

            ${this.currentSlide < this.totalSlides ? `
              <button
                class="quiz-btn quiz-btn-primary"
                onclick="window.histologiaNextSlide()"
              >
                Następny preparat →
              </button>
            ` : `
              <a href="../histologia" class="quiz-btn quiz-btn-primary" style="text-decoration: none;">
                ✓ Zakończ zestaw
              </a>
            `}
          </div>
        </div>
      `;
    }

    revealAnswer() {
      this.answerRevealed = true;
      this.render();
    }

    nextSlide() {
      if (this.currentSlide < this.totalSlides) {
        this.currentSlide++;
        this.answerRevealed = false;
        this.render();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    prevSlide() {
      if (this.currentSlide > 1) {
        this.currentSlide--;
        this.answerRevealed = false;
        this.render();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  }

  // Initialize viewer when DOM is ready
  function initHistologiaViewers() {
    const containers = document.querySelectorAll('[data-histologia-viewer]');
    containers.forEach(container => {
      const viewer = new HistologiaViewer(container);

      // Expose methods globally for onclick handlers
      window.histologiaRevealAnswer = () => viewer.revealAnswer();
      window.histologiaNextSlide = () => viewer.nextSlide();
      window.histologiaPrevSlide = () => viewer.prevSlide();
    });
  }

  // Run on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHistologiaViewers);
  } else {
    initHistologiaViewers();
  }
})();
