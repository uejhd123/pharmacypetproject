function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const toggleIcon = document.getElementById('toggle-icon');
    const toggleIconCreate = document.getElementById('toggle-create-icon');
    const createCollapse = document.getElementById('create-collapse');

    if (sidebar.style.width === '4.5rem') {
        expandSidebar();
        localStorage.setItem('sidebarState', 'expanded');
        if (localStorage.getItem('createSidebarState') === 'expanded') {
            createCollapse.classList.add('show');
            toggleIconCreate.classList.remove('bi-plus-square');
            toggleIconCreate.classList.add('bi-dash-square');
        }
    } else {
        collapseSidebar();
        localStorage.setItem('sidebarState', 'collapsed');
        createCollapse.classList.remove('show');
        toggleIconCreate.classList.remove('bi-dash-square');
        toggleIconCreate.classList.add('bi-plus-square');
    }
}

function expandSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const icons = document.querySelectorAll('.sidebar-icon');
    const texts = document.querySelectorAll('.sidebar-text');
    const sidebarHome = document.querySelectorAll('.sidebar-home');
    const navlink = document.querySelectorAll('.nav-link');
    
    const toggleIcon = document.getElementById('toggle-icon');

    sidebar.style.width = '280px';
    sidebar.classList.add('p-3');
    navlink.forEach(home => {
        home.classList.remove('py-3', 'rounded-0', 'nav-flush', 'text-center');
    });
    sidebarHome.forEach(home => {
        home.classList.add('pb-3', 'mb-3');
        home.classList.remove('p-3');
    });
    icons.forEach(icon => {
        icon.style.fontSize = '16px';
    });
    texts.forEach(text => text.style.display = 'inline');

    toggleIcon.classList.remove('bi-arrows-fullscreen');
    toggleIcon.classList.add('bi-fullscreen-exit');
    toggleIcon.style.fontSize = '16px';
}

function collapseSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const icons = document.querySelectorAll('.sidebar-icon');
    const texts = document.querySelectorAll('.sidebar-text');
    const sidebarHome = document.querySelectorAll('.sidebar-home');
    const navlink = document.querySelectorAll('.nav-link');
    const toggleIcon = document.getElementById('toggle-icon');
    const toggleIconCreate = document.getElementById('toggle-create-icon');

    sidebar.style.width = '4.5rem';
    sidebar.classList.remove('p-3');
    navlink.forEach(home => {
        home.classList.add('py-3', 'rounded-0', 'nav-flush', 'text-center');
    });
    sidebarHome.forEach(home => {
        home.classList.remove('pb-3', 'mb-3');
        home.classList.add('p-3');
    });
    icons.forEach(icon => {
        icon.style.fontSize = '24px';
    });
    texts.forEach(text => text.style.display = 'none');
    toggleIcon.classList.remove('bi-fullscreen-exit');
    toggleIcon.classList.add('bi-arrows-fullscreen');
    toggleIcon.style.fontSize = '24px';

    toggleIconCreate.classList.remove('bi-dash-square');
    toggleIconCreate.classList.add('bi-plus-square');
    localStorage.setItem('createSidebarState', 'collapsed');
}

function toggleCreateSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const toggleIconCreate = document.getElementById('toggle-create-icon');
    const createCollapse = document.getElementById('create-collapse');

    if (sidebar.style.width === '4.5rem') {
        expandSidebar();
        localStorage.setItem('sidebarState', 'expanded');
        createCollapse.classList.add('show');
        toggleIconCreate.classList.remove('bi-plus-square');
        toggleIconCreate.classList.add('bi-dash-square');
        localStorage.setItem('createSidebarState', 'expanded');
    } else {
        createCollapse.classList.toggle('show');
        if (createCollapse.classList.contains('show')) {
            toggleIconCreate.classList.remove('bi-plus-square');
            toggleIconCreate.classList.add('bi-dash-square');
            localStorage.setItem('createSidebarState', 'expanded');
        } else {
            toggleIconCreate.classList.remove('bi-dash-square');
            toggleIconCreate.classList.add('bi-plus-square');
            localStorage.setItem('createSidebarState', 'collapsed');
        }
    }
};