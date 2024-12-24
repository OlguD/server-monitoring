const mobileMenuButton = document.getElementById('mobile-menu-button');
const sidebar = document.getElementById('sidebar');
const overlay = document.createElement('div');

// Overlay oluştur
overlay.className = 'fixed inset-0 bg-black bg-opacity-50 z-30 hidden md:hidden';
document.body.appendChild(overlay);

function toggleSidebar() {
    const isOpen = sidebar.classList.contains('translate-x-0');
    
    if (isOpen) {
        sidebar.classList.remove('translate-x-0');
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
    } else {
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

mobileMenuButton.addEventListener('click', toggleSidebar);
overlay.addEventListener('click', toggleSidebar);

// Ekran boyutu değiştiğinde
window.addEventListener('resize', function() {
    if (window.innerWidth >= 768) {
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
    } else {
        sidebar.classList.add('-translate-x-full');
    }
});