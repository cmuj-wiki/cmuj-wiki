// Simple password gate for CMUJ Wiki
// This is NOT cryptographically secure - it's just a basic deterrent

(function() {
    'use strict';

    // Configuration
    const CORRECT_PASSWORD_HASH = '5f4dcc3b5aa765d61d8327deb882cf99'; // MD5 hash of "password"
    const SESSION_KEY = 'cmuj_wiki_authenticated';

    // Check if already authenticated in this session
    if (sessionStorage.getItem(SESSION_KEY) === 'true') {
        return; // Already authenticated, allow access
    }

    // Hide page content initially
    document.body.style.visibility = 'hidden';

    // Simple MD5 hash function (for basic obfuscation only)
    function simpleHash(str) {
        // You should replace this with actual MD5 or SHA-256
        // For now, using a placeholder
        return str.split('').reduce((a, b) => {
            a = ((a << 5) - a) + b.charCodeAt(0);
            return a & a;
        }, 0).toString(16);
    }

    // Prompt for password
    function checkPassword() {
        const password = prompt('🔒 CMUJ Wiki - Dostęp dla studentów\n\nWprowadź hasło dostępu:');

        if (password === null) {
            // User clicked cancel
            document.body.innerHTML = '<div style="text-align:center; padding:50px; font-family:sans-serif;"><h1>Dostęp zabroniony</h1><p>Ta strona wymaga hasła dostępu.</p></div>';
            document.body.style.visibility = 'visible';
            return;
        }

        // Check password (using simple comparison for now)
        // Change "cmujstudent2025" to your actual password
        if (password === 'cmujstudent2025') {
            sessionStorage.setItem(SESSION_KEY, 'true');
            document.body.style.visibility = 'visible';
        } else {
            alert('❌ Nieprawidłowe hasło!');
            checkPassword(); // Try again
        }
    }

    // Run password check when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkPassword);
    } else {
        checkPassword();
    }
})();
