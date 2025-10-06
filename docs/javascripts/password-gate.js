// Simple password gate for CMUJ Wiki
// This is NOT cryptographically secure - it's just a basic deterrent

(function() {
    'use strict';

    // Configuration
    const STUDENT_PASSWORD = 'wawelskimedyk';
    const ADMIN_PASSWORD = 'totalnyszefpozaadminem';
    const SESSION_KEY = 'cmuj_wiki_authenticated';
    const ROLE_KEY = 'cmuj_wiki_role';

    // Check if already authenticated in this session
    if (sessionStorage.getItem(SESSION_KEY) === 'true') {
        applyRolePermissions(sessionStorage.getItem(ROLE_KEY));
        return; // Already authenticated, allow access
    }

    // Hide page content initially
    document.body.style.visibility = 'hidden';

    // Apply role-based permissions
    function applyRolePermissions(role) {
        if (role === 'student') {
            // Hide edit button for students
            const style = document.createElement('style');
            style.id = 'student-restrictions';
            style.textContent = `
                .md-content__button.md-icon[title*="Edit"] {
                    display: none !important;
                }
                /* Also hide the edit action link */
                a.md-content__button[href*="edit"] {
                    display: none !important;
                }
            `;
            document.head.appendChild(style);
        }
        // Admin role: no restrictions, edit button stays visible
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

        // Check passwords
        if (password === ADMIN_PASSWORD) {
            // Admin access - full permissions
            sessionStorage.setItem(SESSION_KEY, 'true');
            sessionStorage.setItem(ROLE_KEY, 'admin');
            applyRolePermissions('admin');
            document.body.style.visibility = 'visible';
        } else if (password === STUDENT_PASSWORD) {
            // Student access - restricted
            sessionStorage.setItem(SESSION_KEY, 'true');
            sessionStorage.setItem(ROLE_KEY, 'student');
            applyRolePermissions('student');
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
