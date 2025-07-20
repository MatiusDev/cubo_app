// Utilidades para la aplicación
const Utils = {
    /**
     * Guarda datos en localStorage
     * @param {string} key - Clave para almacenar
     * @param {any} value - Valor a almacenar
     */
    saveToLocalStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error al guardar en localStorage:', error);
        }
    },

    /**
     * Obtiene datos de localStorage
     * @param {string} key - Clave a recuperar
     * @param {any} defaultValue - Valor por defecto si no existe
     * @returns {any} - Valor almacenado o valor por defecto
     */
    getFromLocalStorage(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Error al obtener de localStorage:', error);
            return defaultValue;
        }
    },

    /**
     * Elimina datos de localStorage
     * @param {string} key - Clave a eliminar
     */
    removeFromLocalStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Error al eliminar de localStorage:', error);
        }
    },

    /**
     * Carga un archivo JSON
     * @param {string} url - URL del archivo JSON
     * @returns {Promise<Object>} - Datos del JSON
     */
    async fetchJson(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error al cargar ${url}:`, error);
            return null;
        }
    },

    /**
     * Valida y sanitiza texto de entrada
     * @param {string} text - Texto a validar
     * @returns {string} - Texto sanitizado
     */
    sanitizeInput(text) {
        if (typeof text !== 'string') return '';
        
        // Eliminar caracteres peligrosos para prevenir XSS
        return text
            .replace(/[<>]/g, '') // Eliminar < y >
            .replace(/javascript:/gi, '') // Eliminar javascript:
            .replace(/on\w+=/gi, '') // Eliminar event handlers
            .trim();
    },

    /**
     * Valida si un texto contiene solo caracteres seguros
     * @param {string} text - Texto a validar
     * @returns {boolean} - True si es válido
     */
    isValidInput(text) {
        if (typeof text !== 'string') return false;
        
        // Patrón para caracteres seguros
        const safePattern = /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-_.,!?@#$%&*()+=:;'"()[\]{}|\\/]+$/;
        return safePattern.test(text) && text.length <= 1000;
    },

    /**
     * Formatea una fecha
     * @param {Date|string} date - Fecha a formatear
     * @returns {string} - Fecha formateada
     */
    formatDate(date) {
        const d = new Date(date);
        return d.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    /**
     * Genera una fecha actual formateada
     * @returns {string} - Fecha actual formateada
     */
    getCurrentDate() {
        return this.formatDate(new Date());
    },

    /**
     * Busca coincidencias de texto (case-insensitive)
     * @param {string} searchText - Texto a buscar
     * @param {string} content - Contenido donde buscar
     * @returns {boolean} - True si encuentra coincidencia
     */
    searchMatch(searchText, content) {
        if (!searchText || !content) return false;
        
        const search = searchText.toLowerCase().trim();
        const text = content.toLowerCase();
        
        return text.includes(search);
    },

    /**
     * Busca coincidencias en un array de objetos
     * @param {string} searchText - Texto a buscar
     * @param {Array} items - Array de objetos
     * @param {Array} fields - Campos donde buscar
     * @returns {Array} - Elementos que coinciden
     */
    searchInArray(searchText, items, fields) {
        if (!searchText || !items || !Array.isArray(items)) return [];
        
        const search = searchText.toLowerCase().trim();
        
        return items.filter(item => {
            return fields.some(field => {
                const value = item[field];
                if (typeof value === 'string') {
                    return value.toLowerCase().includes(search);
                }
                return false;
            });
        });
    },

    /**
     * Debounce function para optimizar búsquedas
     * @param {Function} func - Función a ejecutar
     * @param {number} wait - Tiempo de espera en ms
     * @returns {Function} - Función debounced
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Muestra una notificación temporal
     * @param {string} message - Mensaje a mostrar
     * @param {string} type - Tipo de notificación (success, error, warning, info)
     * @param {number} duration - Duración en ms
     */
    showNotification(message, type = 'info', duration = 3000) {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification is-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            animation: slideIn 0.3s ease;
        `;
        
        notification.innerHTML = `
            <button class="delete" onclick="this.parentElement.remove()"></button>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        // Auto-eliminar después del tiempo especificado
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 300);
            }
        }, duration);
    },

    /**
     * Genera un ID único
     * @returns {string} - ID único
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * Verifica si estamos en modo móvil
     * @returns {boolean} - True si es móvil
     */
    isMobile() {
        return window.innerWidth <= 768;
    },

    /**
     * Maneja errores de manera consistente
     * @param {Error} error - Error a manejar
     * @param {string} context - Contexto donde ocurrió el error
     */
    handleError(error, context = '') {
        console.error(`Error en ${context}:`, error);
        this.showNotification(
            `Error: ${error.message || 'Algo salió mal'}`,
            'error',
            5000
        );
    }
};

// Agregar estilos CSS para las notificaciones
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyles); 