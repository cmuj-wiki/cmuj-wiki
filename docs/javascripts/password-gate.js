// Simple password gate for CMUJ Wiki
// This is NOT cryptographically secure - it's just a basic deterrent

(function() {
    'use strict';

    // Configuration - MD5 hashes of passwords (not plaintext!)
    // Student password: wawelskimedyk
    const STUDENT_PASSWORD_HASH = 'd5769d43e0aabf243daeab29e4d03a16';
    // Admin password: totalnyszefpozaadminem
    const ADMIN_PASSWORD_HASH = 'e17ef6afb5c056d26d1e02d9f4c32616';

    const SESSION_KEY = 'cmuj_wiki_authenticated';
    const ROLE_KEY = 'cmuj_wiki_role';

    // MD5 hash function (from blueimp-md5)
    function md5(string) {
        function md5cycle(x, k) {
            var a = x[0], b = x[1], c = x[2], d = x[3];
            a = ff(a, b, c, d, k[0], 7, -680876936);
            d = ff(d, a, b, c, k[1], 12, -389564586);
            c = ff(c, d, a, b, k[2], 17, 606105819);
            b = ff(b, c, d, a, k[3], 22, -1044525330);
            a = ff(a, b, c, d, k[4], 7, -176418897);
            d = ff(d, a, b, c, k[5], 12, 1200080426);
            c = ff(c, d, a, b, k[6], 17, -1473231341);
            b = ff(b, c, d, a, k[7], 22, -45705983);
            a = ff(a, b, c, d, k[8], 7, 1770035416);
            d = ff(d, a, b, c, k[9], 12, -1958414417);
            c = ff(c, d, a, b, k[10], 17, -42063);
            b = ff(b, c, d, a, k[11], 22, -1990404162);
            a = ff(a, b, c, d, k[12], 7, 1804603682);
            d = ff(d, a, b, c, k[13], 12, -40341101);
            c = ff(c, d, a, b, k[14], 17, -1502002290);
            b = ff(b, c, d, a, k[15], 22, 1236535329);
            a = gg(a, b, c, d, k[1], 5, -165796510);
            d = gg(d, a, b, c, k[6], 9, -1069501632);
            c = gg(c, d, a, b, k[11], 14, 643717713);
            b = gg(b, c, d, a, k[0], 20, -373897302);
            a = gg(a, b, c, d, k[5], 5, -701558691);
            d = gg(d, a, b, c, k[10], 9, 38016083);
            c = gg(c, d, a, b, k[15], 14, -660478335);
            b = gg(b, c, d, a, k[4], 20, -405537848);
            a = gg(a, b, c, d, k[9], 5, 568446438);
            d = gg(d, a, b, c, k[14], 9, -1019803690);
            c = gg(c, d, a, b, k[3], 14, -187363961);
            b = gg(b, c, d, a, k[8], 20, 1163531501);
            a = gg(a, b, c, d, k[13], 5, -1444681467);
            d = gg(d, a, b, c, k[2], 9, -51403784);
            c = gg(c, d, a, b, k[7], 14, 1735328473);
            b = gg(b, c, d, a, k[12], 20, -1926607734);
            a = hh(a, b, c, d, k[5], 4, -378558);
            d = hh(d, a, b, c, k[8], 11, -2022574463);
            c = hh(c, d, a, b, k[11], 16, 1839030562);
            b = hh(b, c, d, a, k[14], 23, -35309556);
            a = hh(a, b, c, d, k[1], 4, -1530992060);
            d = hh(d, a, b, c, k[4], 11, 1272893353);
            c = hh(c, d, a, b, k[7], 16, -155497632);
            b = hh(b, c, d, a, k[10], 23, -1094730640);
            a = hh(a, b, c, d, k[13], 4, 681279174);
            d = hh(d, a, b, c, k[0], 11, -358537222);
            c = hh(c, d, a, b, k[3], 16, -722521979);
            b = hh(b, c, d, a, k[6], 23, 76029189);
            a = hh(a, b, c, d, k[9], 4, -640364487);
            d = hh(d, a, b, c, k[12], 11, -421815835);
            c = hh(c, d, a, b, k[15], 16, 530742520);
            b = hh(b, c, d, a, k[2], 23, -995338651);
            a = ii(a, b, c, d, k[0], 6, -198630844);
            d = ii(d, a, b, c, k[7], 10, 1126891415);
            c = ii(c, d, a, b, k[14], 15, -1416354905);
            b = ii(b, c, d, a, k[5], 21, -57434055);
            a = ii(a, b, c, d, k[12], 6, 1700485571);
            d = ii(d, a, b, c, k[3], 10, -1894986606);
            c = ii(c, d, a, b, k[10], 15, -1051523);
            b = ii(b, c, d, a, k[1], 21, -2054922799);
            a = ii(a, b, c, d, k[8], 6, 1873313359);
            d = ii(d, a, b, c, k[15], 10, -30611744);
            c = ii(c, d, a, b, k[6], 15, -1560198380);
            b = ii(b, c, d, a, k[13], 21, 1309151649);
            a = ii(a, b, c, d, k[4], 6, -145523070);
            d = ii(d, a, b, c, k[11], 10, -1120210379);
            c = ii(c, d, a, b, k[2], 15, 718787259);
            b = ii(b, c, d, a, k[9], 21, -343485551);
            x[0] = add32(a, x[0]);
            x[1] = add32(b, x[1]);
            x[2] = add32(c, x[2]);
            x[3] = add32(d, x[3]);
        }
        function cmn(q, a, b, x, s, t) {
            a = add32(add32(a, q), add32(x, t));
            return add32((a << s) | (a >>> (32 - s)), b);
        }
        function ff(a, b, c, d, x, s, t) {
            return cmn((b & c) | ((~b) & d), a, b, x, s, t);
        }
        function gg(a, b, c, d, x, s, t) {
            return cmn((b & d) | (c & (~d)), a, b, x, s, t);
        }
        function hh(a, b, c, d, x, s, t) {
            return cmn(b ^ c ^ d, a, b, x, s, t);
        }
        function ii(a, b, c, d, x, s, t) {
            return cmn(c ^ (b | (~d)), a, b, x, s, t);
        }
        function md51(s) {
            var n = s.length, state = [1732584193, -271733879, -1732584194, 271733878], i;
            for (i = 64; i <= s.length; i += 64) {
                md5cycle(state, md5blk(s.substring(i - 64, i)));
            }
            s = s.substring(i - 64);
            var tail = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            for (i = 0; i < s.length; i++)
                tail[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
            tail[i >> 2] |= 0x80 << ((i % 4) << 3);
            if (i > 55) {
                md5cycle(state, tail);
                for (i = 0; i < 16; i++) tail[i] = 0;
            }
            tail[14] = n * 8;
            md5cycle(state, tail);
            return state;
        }
        function md5blk(s) {
            var md5blks = [], i;
            for (i = 0; i < 64; i += 4) {
                md5blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24);
            }
            return md5blks;
        }
        var hex_chr = '0123456789abcdef'.split('');
        function rhex(n) {
            var s = '', j = 0;
            for (; j < 4; j++)
                s += hex_chr[(n >> (j * 8 + 4)) & 0x0F] + hex_chr[(n >> (j * 8)) & 0x0F];
            return s;
        }
        function hex(x) {
            for (var i = 0; i < x.length; i++)
                x[i] = rhex(x[i]);
            return x.join('');
        }
        function add32(a, b) {
            return (a + b) & 0xFFFFFFFF;
        }
        return hex(md51(string));
    }

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

        // Hash the entered password and compare
        const passwordHash = md5(password);

        if (passwordHash === ADMIN_PASSWORD_HASH) {
            // Admin access - full permissions
            sessionStorage.setItem(SESSION_KEY, 'true');
            sessionStorage.setItem(ROLE_KEY, 'admin');
            applyRolePermissions('admin');
            document.body.style.visibility = 'visible';
            showInstallPrompt(); // Show PWA install prompt
        } else if (passwordHash === STUDENT_PASSWORD_HASH) {
            // Student access - restricted
            sessionStorage.setItem(SESSION_KEY, 'true');
            sessionStorage.setItem(ROLE_KEY, 'student');
            applyRolePermissions('student');
            document.body.style.visibility = 'visible';
            showInstallPrompt(); // Show PWA install prompt
        } else {
            alert('❌ Nieprawidłowe hasło!');
            checkPassword(); // Try again
        }
    }

    // ============================================================================
    // PWA INSTALL PROMPT
    // ============================================================================

    let deferredPrompt = null;

    // Capture the install prompt event
    window.addEventListener('beforeinstallprompt', (e) => {
        console.log('[PWA] beforeinstallprompt event captured');
        e.preventDefault();
        deferredPrompt = e;
    });

    // Show custom install prompt after successful login
    function showInstallPrompt() {
        // Check if prompt should be shown
        const promptShown = localStorage.getItem('pwa_install_prompt_shown');
        const promptDismissed = sessionStorage.getItem('pwa_install_dismissed');

        if (deferredPrompt && !promptShown && !promptDismissed) {
            console.log('[PWA] Showing install prompt');

            // Create modal
            const modal = document.createElement('div');
            modal.id = 'pwa-install-modal';
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 999999;
                animation: fadeIn 0.3s ease;
            `;

            modal.innerHTML = `
                <div style="
                    background: white;
                    border-radius: 16px;
                    padding: 30px;
                    max-width: 400px;
                    margin: 20px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    text-align: center;
                    color: #333;
                ">
                    <div style="font-size: 48px; margin-bottom: 20px;">📱</div>
                    <h2 style="margin: 0 0 15px 0; color: #5c6bc0; font-size: 24px;">
                        Zainstaluj aplikację!
                    </h2>
                    <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.5; color: #666;">
                        Możesz teraz zainstalować CMUJ Wiki na swoim telefonie!<br>
                        Szybszy dostęp i działanie offline.
                    </p>
                    <button id="pwa-install-btn" style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        font-size: 16px;
                        font-weight: bold;
                        border-radius: 8px;
                        cursor: pointer;
                        margin: 0 10px 10px 0;
                        transition: transform 0.2s;
                    " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        🚀 Zainstaluj teraz
                    </button>
                    <button id="pwa-dismiss-btn" style="
                        background: transparent;
                        color: #666;
                        border: 1px solid #ddd;
                        padding: 15px 30px;
                        font-size: 16px;
                        border-radius: 8px;
                        cursor: pointer;
                        transition: all 0.2s;
                    " onmouseover="this.style.background='#f5f5f5'" onmouseout="this.style.background='transparent'">
                        Może później
                    </button>
                </div>
            `;

            document.body.appendChild(modal);

            // Install button handler
            document.getElementById('pwa-install-btn').addEventListener('click', async () => {
                console.log('[PWA] Install button clicked');
                modal.remove();

                // Show browser's install prompt
                deferredPrompt.prompt();

                // Wait for user's response
                const { outcome } = await deferredPrompt.userChoice;
                console.log('[PWA] User response:', outcome);

                // Mark as shown (don't show again)
                localStorage.setItem('pwa_install_prompt_shown', 'true');
                deferredPrompt = null;
            });

            // Dismiss button handler
            document.getElementById('pwa-dismiss-btn').addEventListener('click', () => {
                console.log('[PWA] Install prompt dismissed');
                modal.remove();
                // Mark as dismissed for this session only
                sessionStorage.setItem('pwa_install_dismissed', 'true');
            });
        }
    }

    // ============================================================================
    // SERVICE WORKER REGISTRATION
    // ============================================================================

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/cmuj-wiki/sw.js')
                .then(registration => {
                    console.log('[PWA] Service Worker registered:', registration.scope);
                })
                .catch(error => {
                    console.error('[PWA] Service Worker registration failed:', error);
                });
        });
    }

    // Run password check when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkPassword);
    } else {
        checkPassword();
    }
})();
