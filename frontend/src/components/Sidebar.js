import { Utils } from '../utils.js'

// Componente de la barra lateral
export class Sidebar {
    constructor() {
        this.isCollapsed = false;
        this.currentSection = 'balances';
        this.sections = [
            {
                id: 'balances',
                title: 'Saldos',
                icon: 'fas fa-chart-pie',
                route: '/balances'
            },
            {
                id: 'sales',
                title: 'Ventas',
                icon: 'fas fa-chart-line',
                route: '/sales'
            },
            {
                id: 'inventory',
                title: 'Inventario',
                icon: 'fas fa-boxes',
                route: '/inventory'
            },
            {
                id: 'customers',
                title: 'Clientes',
                icon: 'fas fa-users',
                route: '/customers'
            },
            {
                id: 'reports',
                title: 'Reportes',
                icon: 'fas fa-file-alt',
                route: '/reports'
            },
            {
                id: 'test',
                title: 'Test',
                icon: 'fas fa-flask',
                route: '/test'
            },
            {
                id: 'settings',
                title: 'Configuración',
                icon: 'fas fa-cog',
                route: '/settings'
            }
        ];
        
        // Pequeño delay para asegurar que el DOM esté listo
        setTimeout(() => {
            this.init();
        }, 10);
    }

    init() {
        this.loadState();
        this.render();
        this.bindEvents();
        this.updateActiveSection();
        this.updateSidebarState(); // Asegurar que el estado visual se aplique
    }

    render() {
        const sidebarNav = document.getElementById('sidebarNav');
        if (!sidebarNav) return;

        const navItems = this.sections.map(section => `
            <a href="#" class="nav-item" data-section="${section.id}" data-route="${section.route}">
                <i class="${section.icon} nav-icon"></i>
                <span class="nav-text">${section.title}</span>
            </a>
        `).join('');

        sidebarNav.innerHTML = navItems;
    }

    bindEvents() {
        // Toggle de la barra lateral
        const toggleBtn = document.getElementById('sidebarToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Navegación por secciones
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const sectionId = item.dataset.section;
                this.navigateToSection(sectionId);
            });
        });

        // Manejo de eventos de teclado
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'b') {
                e.preventDefault();
                this.toggleSidebar();
            }
        });

        // Responsive: cerrar sidebar en móvil al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (Utils.isMobile() && this.isCollapsed === false) {
                const sidebar = document.getElementById('sidebar');
                const isClickInsideSidebar = sidebar && sidebar.contains(e.target);
                const isClickOnToggle = e.target.closest('#sidebarToggle');
                
                if (!isClickInsideSidebar && !isClickOnToggle) {
                    this.closeMobileSidebar();
                }
            }
        });

        // Redimensionar ventana
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.closeMobileSidebar();
            }
        });
    }

    toggleSidebar() {
        this.isCollapsed = !this.isCollapsed;
        this.updateSidebarState();
        this.saveState();
    }

    updateSidebarState() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('mainContent');
        
        if (sidebar) {
            sidebar.classList.toggle('collapsed', this.isCollapsed);
        }
        
        if (mainContent) {
            mainContent.classList.toggle('sidebar-collapsed', this.isCollapsed);
        }

        // Actualizar logo y título
        const logo = document.getElementById('sidebarLogo');
        const title = document.getElementById('sidebarTitle');
        
        if (logo) {
            logo.style.display = this.isCollapsed ? 'none' : 'block';
        }
        
        if (title) {
            title.style.display = this.isCollapsed ? 'none' : 'block';
        }
    }

    navigateToSection(sectionId) {
        this.currentSection = sectionId;
        this.updateActiveSection();
        this.saveState();
        
        // Disparar evento personalizado para que la app principal maneje la navegación
        const event = new CustomEvent('sectionChanged', {
            detail: { sectionId, section: this.getSectionById(sectionId) }
        });
        document.dispatchEvent(event);
    }

    updateActiveSection() {
        // Remover clase activa de todos los elementos
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => item.classList.remove('active'));

        // Agregar clase activa al elemento actual
        const activeItem = document.querySelector(`[data-section="${this.currentSection}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    getSectionById(sectionId) {
        return this.sections.find(section => section.id === sectionId);
    }

    getCurrentSection() {
        return this.getSectionById(this.currentSection);
    }

    getAllSections() {
        return this.sections;
    }

    closeMobileSidebar() {
        if (Utils.isMobile()) {
            const sidebar = document.getElementById('sidebar');
            if (sidebar) {
                sidebar.classList.remove('mobile-open');
            }
        }
    }

    openMobileSidebar() {
        if (Utils.isMobile()) {
            const sidebar = document.getElementById('sidebar');
            if (sidebar) {
                sidebar.classList.add('mobile-open');
            }
        }
    }

    saveState() {
        Utils.saveToLocalStorage('sidebarCollapsed', this.isCollapsed);
        Utils.saveToLocalStorage('currentSection', this.currentSection);
    }

    loadState() {
        this.isCollapsed = Utils.getFromLocalStorage('sidebarCollapsed', false);
        this.currentSection = Utils.getFromLocalStorage('currentSection', 'balances');
    }

    // Método público para cambiar sección desde fuera
    setActiveSection(sectionId) {
        if (this.sections.find(s => s.id === sectionId)) {
            this.currentSection = sectionId;
            this.updateActiveSection();
            this.saveState();
        }
    }

    // Método para obtener el estado de colapso
    isSidebarCollapsed() {
        return this.isCollapsed;
    }
} 