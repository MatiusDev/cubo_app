import { Utils } from './utils.js'

// Aplicación principal TUYA Fast-Data
export class App {
    constructor() {
        this.isInitialized = false;
        this.init();
    }

    async init() {
        try {
            // Esperar a que el DOM esté listo
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.initializeApp();
                });
            } else {
                this.initializeApp();
            }
        } catch (error) {
            Utils.handleError(error, 'Inicialización de la aplicación');
        }
    }

    async initializeApp() {
        if (this.isInitialized) return;

        try {
            // Inicializar componentes
            await this.initializeComponents();
            
            // Configurar estado inicial
            this.setupInitialState();
            
            // Configurar eventos globales
            this.setupGlobalEvents();
            
            // Cargar datos iniciales
            await this.loadInitialData();
            
            // Marcar como inicializada
            this.isInitialized = true;
            
            // Mostrar notificación de bienvenida
            Utils.showNotification('¡Bienvenido a TUYA Fast-Data!', 'success', 2000);
            
            console.log('Aplicación TUYA Fast-Data inicializada correctamente');

        } catch (error) {
            Utils.handleError(error, 'Inicialización de la aplicación');
        }
    }

    async initializeComponents() {
        try {
            // Verificar que todos los componentes estén disponibles
            if (typeof window.sidebar === 'undefined') {
                throw new Error('Componente Sidebar no está disponible');
            }
            if (typeof window.navbar === 'undefined') {
                throw new Error('Componente Navbar no está disponible');
            }
            if (typeof window.sectionContent === 'undefined') {
                throw new Error('Componente SectionContent no está disponible');
            }

            // Los componentes ya se inicializan automáticamente en sus constructores
            // No es necesario llamar init() nuevamente

        } catch (error) {
            Utils.handleError(error, 'Inicializar componentes');
        }
    }

    setupInitialState() {
        try {
            // El estado inicial ya se carga automáticamente en el constructor del Sidebar
            // No es necesario cargarlo nuevamente aquí

        } catch (error) {
            Utils.handleError(error, 'Configurar estado inicial');
        }
    }

    setupGlobalEvents() {
        // Manejar errores no capturados
        window.addEventListener('error', (e) => {
            Utils.handleError(e.error, 'Error global');
        });

        // Manejar promesas rechazadas
        window.addEventListener('unhandledrejection', (e) => {
            Utils.handleError(new Error(e.reason), 'Promesa rechazada');
        });

        // Manejar cambios de sección
        document.addEventListener('sectionChanged', (e) => {
            this.handleSectionChange(e.detail);
        });

        // Manejar eventos de teclado globales
        document.addEventListener('keydown', (e) => {
            this.handleGlobalKeydown(e);
        });

        // Manejar eventos de redimensionamiento
        window.addEventListener('resize', Utils.debounce(() => {
            this.handleResize();
        }, 250));
    }

    async loadInitialData() {
        try {
            // Los datos iniciales ya se cargan automáticamente en los constructores de los componentes
            // No es necesario cargar datos adicionales aquí

        } catch (error) {
            Utils.handleError(error, 'Cargar datos iniciales');
        }
    }

    handleSectionChange(detail) {
        const { sectionId, section } = detail;
        
        try {
            // Actualizar título de la página
            window.navbar.updatePageTitle(this.getSectionTitle(sectionId));
            
            // Cargar contenido de la sección
            if (window.sectionContent) {
                window.sectionContent.loadSection(sectionId);
            }
            
            // Actualizar URL sin recargar la página
            this.updateURL(sectionId);
            
        } catch (error) {
            Utils.handleError(error, `Cambio de sección a ${sectionId}`);
        }
    }

    handleGlobalKeydown(e) {
        // Atajos de teclado globales
        switch (e.key) {
            case 'Escape':
                // Cerrar modales
                this.closeAllModals();
                break;
            case 'F5':
                // Prevenir recarga de página
                e.preventDefault();
                Utils.showNotification('Usa Ctrl+R para recargar', 'info');
                break;
        }
    }

    handleResize() {
        // Manejar cambios de tamaño de ventana
        if (Utils.isMobile()) {
            // En móvil, cerrar sidebar si está abierta
            if (window.sidebar && !window.sidebar.isSidebarCollapsed()) {
                window.sidebar.closeMobileSidebar();
            }
        }
    }

    updateURL(sectionId) {
        try {
            // Actualizar URL sin recargar la página
            const newURL = `${window.location.pathname}#${sectionId}`;
            window.history.pushState({ sectionId }, '', newURL);
        } catch (error) {
            console.warn('No se pudo actualizar la URL:', error);
        }
    }

    closeAllModals() {
        // Cerrar todos los modales abiertos
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => modal.remove());
    }

    getSectionTitle(sectionId) {
        const titles = {
            balances: 'Saldos',
            sales: 'Ventas',
            inventory: 'Inventario',
            customers: 'Clientes',
            reports: 'Reportes',
            test: 'Test',
            settings: 'Configuración'
        };
        return titles[sectionId] || sectionId;
    }

    // Métodos de utilidad pública
    getAppInfo() {
        return {
            name: 'TUYA Fast-Data',
            version: '1.0.0',
            initialized: this.isInitialized,
            currentSection: window.sidebar ? window.sidebar.getCurrentSection() : null,
            sidebarCollapsed: window.sidebar ? window.sidebar.isSidebarCollapsed() : false
        };
    }

    // Método para reiniciar la aplicación
    async restart() {
        try {
            this.isInitialized = false;
            
            // Limpiar localStorage
            localStorage.clear();
            
            // Recargar la página
            window.location.reload();
            
        } catch (error) {
            Utils.handleError(error, 'Reiniciar aplicación');
        }
    }

    // Método para exportar datos de la aplicación
    exportAppData() {
        try {
            const data = {
                settings: {
                    sidebarCollapsed: window.sidebar ? window.sidebar.isSidebarCollapsed() : false,
                    currentSection: window.sidebar ? window.sidebar.getCurrentSection() : null
                },
                exportDate: new Date().toISOString()
            };
            
            return JSON.stringify(data, null, 2);
            
        } catch (error) {
            Utils.handleError(error, 'Exportar datos');
            return null;
        }
    }

    // Método para importar datos de la aplicación
    importAppData(dataString) {
        try {
            const data = JSON.parse(dataString);
            
            // Importar configuraciones
            if (data.settings) {
                if (data.settings.sidebarCollapsed !== undefined) {
                    Utils.saveToLocalStorage('sidebarCollapsed', data.settings.sidebarCollapsed);
                }
                if (data.settings.currentSection) {
                    Utils.saveToLocalStorage('currentSection', data.settings.currentSection.id);
                }
            }
            
            Utils.showNotification('Datos importados exitosamente', 'success');
            return true;
            
        } catch (error) {
            Utils.handleError(error, 'Importar datos');
            return false;
        }
    }
} 