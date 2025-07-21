// Utilidades para TUYA Fast-Data - Estilo Funcional/Declarativo

// Gestión de localStorage
const saveToLocalStorage = (key, value) => {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Error al guardar en localStorage:', error);
        return false;
    }
};

const getFromLocalStorage = (key, defaultValue = null) => {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error al leer de localStorage:', error);
        return defaultValue;
    }
};

const removeFromLocalStorage = (key) => {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Error al eliminar de localStorage:', error);
        return false;
    }
};

// Fetch JSON con manejo de errores
const fetchJson = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${url}:`, error);
        return null;
    }
};

// Sanitización de entrada
const sanitizeInput = (input) => {
    if (typeof input !== 'string') return '';
    
    return input
        .replace(/[<>]/g, '') // Remover < y >
        .trim();
};

// Validación de entrada
const isValidInput = (input) => {
    if (typeof input !== 'string') return false;
    if (input.trim().length === 0) return false;
    if (input.length > 1000) return false; // Límite de caracteres
    return true;
};

// Debounce para optimizar búsquedas
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Notificaciones
const showNotification = (message, type = 'info', duration = 3000) => {
    // Remover notificaciones existentes
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    // Crear nueva notificación
    const notification = document.createElement('div');
    notification.className = `notification is-${type}`;
    
    const deleteButton = document.createElement('button');
    deleteButton.className = 'delete';
    deleteButton.onclick = () => notification.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    
    notification.appendChild(deleteButton);
    notification.appendChild(messageDiv);
    
    document.body.appendChild(notification);

    // Auto-remover después del tiempo especificado
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }
};

// Manejo de errores
const handleError = (error, context = '') => {
    console.error(`Error en ${context}:`, error);
    showNotification(`Error: ${error.message}`, 'danger');
};

// Detección de dispositivo móvil
const isMobile = () => {
    return window.innerWidth <= 768;
};

// Generación de ID único
const generateId = () => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

// Formateo de fechas
const formatDate = (date) => {
    if (!date) return '';
    
    const d = new Date(date);
    return d.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

// Formateo de fechas cortas
const formatShortDate = (date) => {
    if (!date) return '';
    
    const d = new Date(date);
    return d.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

// Capitalizar primera letra
const capitalize = (str) => {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

// Truncar texto
const truncateText = (text, maxLength = 100) => {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
};

// Validar email
const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

// Validar URL
const isValidUrl = (url) => {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
};

// Copiar al portapapeles
const copyToClipboard = async (text) => {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copiado al portapapeles', 'success');
        return true;
    } catch (error) {
        console.error('Error al copiar:', error);
        return false;
    }
};

// Descargar archivo
const downloadFile = (content, filename, type = 'text/plain') => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

// Leer archivo
const readFile = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsText(file);
    });
};

// Esperar un tiempo específico
const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

// Retry con backoff exponencial
const retry = async (fn, maxRetries = 3, delay = 1000) => {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await sleep(delay * Math.pow(2, i));
        }
    }
};

// Validar objeto
const isValidObject = (obj) => {
    return obj !== null && typeof obj === 'object' && !Array.isArray(obj);
};

// Validar array
const isValidArray = (arr) => {
    return Array.isArray(arr) && arr.length > 0;
};

// Merge objetos
const mergeObjects = (...objects) => {
    return objects.reduce((result, obj) => {
        if (isValidObject(obj)) {
            return { ...result, ...obj };
        }
        return result;
    }, {});
};

// Filtrar objeto
const filterObject = (obj, predicate) => {
    return Object.fromEntries(
        Object.entries(obj).filter(([key, value]) => predicate(key, value))
    );
};

// Obtener valor anidado de objeto
const getNestedValue = (obj, path, defaultValue = undefined) => {
    return path.split('.').reduce((current, key) => {
        return current && current[key] !== undefined ? current[key] : defaultValue;
    }, obj);
};

// Establecer valor anidado en objeto
const setNestedValue = (obj, path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const target = keys.reduce((current, key) => {
        if (!current[key] || typeof current[key] !== 'object') {
            current[key] = {};
        }
        return current[key];
    }, obj);
    target[lastKey] = value;
    return obj;
};

// Exportar objeto con todas las utilidades
export const Utils = {
    // localStorage
    saveToLocalStorage,
    getFromLocalStorage,
    removeFromLocalStorage,
    
    // Fetch y validación
    fetchJson,
    sanitizeInput,
    isValidInput,
    
    // Utilidades de UI
    debounce,
    showNotification,
    handleError,
    
    // Detección y generación
    isMobile,
    generateId,
    
    // Formateo
    formatDate,
    formatShortDate,
    capitalize,
    truncateText,
    
    // Validación
    isValidEmail,
    isValidUrl,
    
    // Archivos y portapapeles
    copyToClipboard,
    downloadFile,
    readFile,
    
    // Control de flujo
    sleep,
    retry,
    
    // Manipulación de objetos
    isValidObject,
    isValidArray,
    mergeObjects,
    filterObject,
    getNestedValue,
    setNestedValue
}; 