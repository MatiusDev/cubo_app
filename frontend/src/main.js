// Importar estilos
import './style.css'

// Importar componentes
import { App } from './app.js'
import { Sidebar } from './components/Sidebar.js'
import { Navbar } from './components/Navbar.js'
import { SectionContent } from './components/SectionContent.js'
import { Utils } from './utils.js'

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Crear instancias globales
    window.sidebar = new Sidebar()
    window.navbar = new Navbar()
    window.sectionContent = new SectionContent()
    window.app = new App()
    window.Utils = Utils

    // Exponer métodos útiles globalmente
    window.TUYAApp = {
        app: window.app,
        sidebar: window.sidebar,
        navbar: window.navbar,
        sectionContent: window.sectionContent,
        Utils: window.Utils
    }

    // Funciones globales de utilidad
    window.showAppInfo = function() {
        const info = app.getAppInfo()
        console.log('Información de la aplicación:', info)
        Utils.showNotification(`App: ${info.name} v${info.version}`, 'info')
    }

    window.restartApp = function() {
        if (confirm('¿Estás seguro de que quieres reiniciar la aplicación?')) {
            app.restart()
        }
    }

    window.exportAppData = function() {
        const data = app.exportAppData()
        if (data) {
            const blob = new Blob([data], { type: 'application/json' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `tuya-app-data-${new Date().toISOString().split('T')[0]}.json`
            a.click()
            URL.revokeObjectURL(url)
            Utils.showNotification('Datos exportados exitosamente', 'success')
        }
    }

    window.importAppData = function() {
        const input = document.createElement('input')
        input.type = 'file'
        input.accept = '.json'
        input.onchange = function(e) {
            const file = e.target.files[0]
            if (file) {
                const reader = new FileReader()
                reader.onload = function(e) {
                    const success = app.importAppData(e.target.result)
                    if (success) {
                        setTimeout(() => {
                            window.location.reload()
                        }, 1000)
                    }
                }
                reader.readAsText(file)
            }
        }
        input.click()
    }

    console.log('TUYA Fast-Data inicializada con Vite')
    
    // Verificación adicional del botón sidebar
    setTimeout(() => {
        const toggleBtn = document.getElementById('sidebarToggle');
        if (toggleBtn) {
            console.log('✅ Botón sidebarToggle encontrado y funcional');
        } else {
            console.error('❌ Botón sidebarToggle no encontrado');
        }
    }, 100);
}) 