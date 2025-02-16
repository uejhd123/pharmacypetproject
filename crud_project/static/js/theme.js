$(document).ready(function() {
    if (localStorage.getItem('sidebarState') === 'collapsed') {
        collapseSidebar();
    } else {
        expandSidebar();
    }

    if (localStorage.getItem('createSidebarState') === 'expanded') {
        const createCollapse = document.getElementById('create-collapse');
        const toggleIconCreate = document.getElementById('toggle-create-icon');
        createCollapse.classList.add('show');
        toggleIconCreate.classList.remove('bi-plus-square');
        toggleIconCreate.classList.add('bi-dash-square');
    }

    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', currentTheme);
    updateThemeToggleText(currentTheme);
});


function updateThemeToggleText(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    const toggleThemeIcon = document.getElementById('toggle-theme');

    if (theme === 'dark') {
        themeToggle.querySelector('.sidebar-text').innerText = 'Светлая тема';
        toggleThemeIcon.classList.remove('bi-sun');
        toggleThemeIcon.classList.add('bi-moon');
    } else {
        themeToggle.querySelector('.sidebar-text').innerText = 'Темная тема';
        toggleThemeIcon.classList.remove('bi-moon');
        toggleThemeIcon.classList.add('bi-sun');
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeToggleText(newTheme);
};


