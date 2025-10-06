/**
 * PWA Install Button - Persistent header button for app installation
 * Replaces the automatic popup with user-initiated install action
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        const installButton = document.getElementById('pwa-install-button');
        const iosModal = document.getElementById('pwa-ios-instructions');
        const iosCloseButton = document.getElementById('pwa-ios-close');

        if (!installButton) {
            console.log('[PWA Install] Button element not found');
            return;
        }

        // Access the global deferredPrompt from password-gate.js
        let deferredPrompt = window.deferredPrompt || null;

        // ====================================================================
        // 1. Check if app is already installed
        // ====================================================================
        const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
                            window.navigator.standalone === true;

        if (isStandalone) {
            console.log('[PWA Install] App already installed, hiding button');
            installButton.style.display = 'none';
            return;
        }

        // ====================================================================
        // 2. iOS Detection
        // ====================================================================
        function isIOS() {
            const platforms = [
                'iPad Simulator',
                'iPhone Simulator',
                'iPod Simulator',
                'iPad',
                'iPhone',
                'iPod'
            ];

            // Check platform
            if (platforms.includes(navigator.platform)) {
                return true;
            }

            // iPad on iOS 13+ detection
            if (navigator.userAgent.includes('Mac') && 'ontouchend' in document) {
                return true;
            }

            return false;
        }

        // ====================================================================
        // 3. Listen for beforeinstallprompt (Chrome/Android)
        // ====================================================================
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('[PWA Install] beforeinstallprompt event captured');
            e.preventDefault();
            deferredPrompt = e;
            window.deferredPrompt = e; // Store globally

            // Show the install button
            installButton.style.display = 'flex';
        });

        // ====================================================================
        // 4. Show button on iOS immediately
        // ====================================================================
        if (isIOS() && !isStandalone) {
            console.log('[PWA Install] iOS detected, showing button');
            installButton.style.display = 'flex';
        }

        // ====================================================================
        // 5. Handle install button click
        // ====================================================================
        installButton.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('[PWA Install] Install button clicked');

            if (deferredPrompt) {
                // Chrome/Android - trigger native install prompt
                console.log('[PWA Install] Triggering native install prompt');
                deferredPrompt.prompt();

                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('[PWA Install] User accepted install');
                    } else {
                        console.log('[PWA Install] User dismissed install');
                    }

                    // Clear the deferred prompt
                    deferredPrompt = null;
                    window.deferredPrompt = null;

                    // Hide button
                    installButton.style.display = 'none';
                });
            } else if (isIOS()) {
                // iOS - show instructions modal
                console.log('[PWA Install] Showing iOS instructions');
                if (iosModal) {
                    iosModal.style.display = 'flex';
                }
            } else {
                console.log('[PWA Install] No install method available');
            }
        });

        // ====================================================================
        // 6. iOS Modal close handlers
        // ====================================================================
        if (iosCloseButton) {
            iosCloseButton.addEventListener('click', () => {
                console.log('[PWA Install] Closing iOS instructions');
                if (iosModal) {
                    iosModal.style.display = 'none';
                }
            });
        }

        if (iosModal) {
            // Close on overlay click
            iosModal.addEventListener('click', (e) => {
                if (e.target === iosModal || e.target.classList.contains('pwa-modal-overlay')) {
                    iosModal.style.display = 'none';
                }
            });

            // Close on Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && iosModal.style.display === 'flex') {
                    iosModal.style.display = 'none';
                }
            });
        }

        // ====================================================================
        // 7. Hide button after successful installation
        // ====================================================================
        window.addEventListener('appinstalled', () => {
            console.log('[PWA Install] App successfully installed');
            installButton.style.display = 'none';
            deferredPrompt = null;
            window.deferredPrompt = null;
        });

        console.log('[PWA Install] Initialized');
    }
})();
