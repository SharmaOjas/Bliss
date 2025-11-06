function toggleMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        if (menu.style.width === '100%') {
            closeMenu();
        } else {
            openMenu();
        }
    }
}

function openMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.style.width = '100%';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.style.width = '0%';
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Close menu when clicking outside the overlay content
document.addEventListener('DOMContentLoaded', function() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.addEventListener('click', function(e) {
            if (e.target === menu) {
                closeMenu();
            }
        });
    }

    // Close menu when clicking on a link
    document.querySelectorAll('.overlay a').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Close menu with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMenu();
        }
    });
});