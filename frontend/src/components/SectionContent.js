import { Utils } from '../utils.js'

// Componente base para el contenido de cada sección
export class SectionContent {
    constructor() {
        this.currentSection = null;
        this.init();
    }

    init() {
        // Inicializar funcionalidades básicas
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Eventos globales si es necesario
    }

    async loadSection(sectionId) {
        try {
            this.currentSection = sectionId;
            
            // Renderizar contenido de la sección
            await this.renderSectionContent(sectionId);
            
            // Inicializar funcionalidades específicas
            this.initializeSectionFeatures(sectionId);
            
        } catch (error) {
            Utils.handleError(error, `Cargar sección ${sectionId}`);
        }
    }

    async renderSectionContent(sectionId) {
        const mainContent = document.getElementById('mainContent');
        if (!mainContent) return;

        let content = '';

        switch (sectionId) {
            case 'balances':
                content = this.getBalancesContent();
                break;
            case 'sales':
                content = this.getSalesContent();
                break;
            case 'inventory':
                content = this.getInventoryContent();
                break;
            case 'customers':
                content = this.getCustomersContent();
                break;
            case 'reports':
                content = this.getReportsContent();
                break;
            case 'test':
                content = this.getTestContent();
                break;
            case 'settings':
                content = this.getSettingsContent();
                break;
            default:
                content = this.getDefaultContent(sectionId);
        }

        mainContent.innerHTML = content;
    }

    initializeSectionFeatures(sectionId) {
        // Inicializar funcionalidades específicas según la sección
        if (sectionId === 'test') {
            this.initializeTestSection();
        }
    }

    getBalancesContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Saldos</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-chart-bar fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Indicador de Saldos</h3>
                            <p class="subtitle is-6 has-text-grey-light">Aquí se mostrará el indicador visual</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getSalesContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Ventas</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-chart-line fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Indicador de Ventas</h3>
                            <p class="subtitle is-6 has-text-grey-light">Aquí se mostrará el indicador visual</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getInventoryContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Inventario</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-boxes fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Indicador de Inventario</h3>
                            <p class="subtitle is-6 has-text-grey-light">Aquí se mostrará el indicador visual</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getCustomersContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Clientes</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-users fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Indicador de Clientes</h3>
                            <p class="subtitle is-6 has-text-grey-light">Aquí se mostrará el indicador visual</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getReportsContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Reportes</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-file-alt fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Indicador de Reportes</h3>
                            <p class="subtitle is-6 has-text-grey-light">Aquí se mostrará el indicador visual</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getTestContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Test</h2>
                </div>
                <div class="card-content">
                    <div class="test-section">
                        <div class="field">
                            <label class="label">Seleccionar archivo Excel</label>
                            <div class="control">
                                <div class="file has-name is-fullwidth">
                                    <label class="file-label">
                                        <input class="file-input" 
                                               type="file" 
                                               id="excelFileInput"
                                               accept=".xlsx,.xls,.csv">
                                        <span class="file-cta">
                                            <span class="file-icon">
                                                <i class="fas fa-file-excel"></i>
                                            </span>
                                            <span class="file-label">
                                                Elegir archivo Excel...
                                            </span>
                                        </span>
                                        <span class="file-name" id="fileName">
                                            Ningún archivo seleccionado
                                        </span>
                                    </label>
                                </div>
                            </div>
                            <p class="help">Formatos soportados: .xlsx, .xls, .csv</p>
                        </div>
                        
                        <div class="field">
                            <div class="control">
                                <button class="button is-primary" id="sendTestBtn" disabled>
                                    <span class="icon">
                                        <i class="fas fa-upload"></i>
                                    </span>
                                    <span>Enviar Excel al Backend</span>
                                </button>
                            </div>
                        </div>
                        
                        <div class="field" id="testResponseArea" style="display: none;">
                            <label class="label">Respuesta del Backend</label>
                            <div class="control">
                                <div class="box" id="testResponseContent">
                                    <!-- Aquí se mostrará la respuesta -->
                                </div>
                            </div>
                        </div>
                        
                        <div class="field" id="testErrorArea" style="display: none;">
                            <div class="notification is-danger" id="testErrorContent">
                                <!-- Aquí se mostrarán los errores -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getSettingsContent() {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">Configuración</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-cog fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Configuración</h3>
                            <p class="subtitle is-6 has-text-grey-light">Aquí se mostrarán las opciones de configuración</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getDefaultContent(sectionId) {
        return `
            <div class="content-card">
                <div class="card-header">
                    <h2 class="card-title">${sectionId}</h2>
                </div>
                <div class="card-content">
                    <div class="indicator-area" id="indicatorArea">
                        <div class="has-text-centered">
                            <i class="fas fa-question-circle fa-3x has-text-grey-light mb-4"></i>
                            <h3 class="title is-4 has-text-grey">Sección ${sectionId}</h3>
                            <p class="subtitle is-6 has-text-grey-light">Contenido no disponible</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
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

    // Método para actualizar el área de indicador
    updateIndicatorArea(content) {
        const indicatorArea = document.getElementById('indicatorArea');
        if (indicatorArea) {
            indicatorArea.innerHTML = content;
        }
    }

    // Método para obtener la sección actual
    getCurrentSection() {
        return this.currentSection;
    }

    // Método para verificar si una sección está cargada
    isSectionLoaded(sectionId) {
        return this.currentSection === sectionId;
    }

    // Método para inicializar la sección Test
    initializeTestSection() {
        const sendTestBtn = document.getElementById('sendTestBtn');
        const fileInput = document.getElementById('excelFileInput');
        const fileName = document.getElementById('fileName');

        if (sendTestBtn) {
            sendTestBtn.addEventListener('click', () => {
                this.sendExcelToBackend();
            });
        }

        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    // Validar tipo de archivo
                    const validTypes = [
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
                        'application/vnd.ms-excel', // .xls
                        'text/csv', // .csv
                        'application/csv' // .csv alternativo
                    ];
                    
                    if (validTypes.includes(file.type) || 
                        file.name.endsWith('.xlsx') || 
                        file.name.endsWith('.xls') || 
                        file.name.endsWith('.csv')) {
                        
                        fileName.textContent = file.name;
                        sendTestBtn.disabled = false;
                        Utils.showNotification(`Archivo seleccionado: ${file.name}`, 'success');
                    } else {
                        fileName.textContent = 'Ningún archivo seleccionado';
                        sendTestBtn.disabled = true;
                        Utils.showNotification('Por favor, selecciona un archivo Excel válido (.xlsx, .xls, .csv)', 'warning');
                        fileInput.value = '';
                    }
                } else {
                    fileName.textContent = 'Ningún archivo seleccionado';
                    sendTestBtn.disabled = true;
                }
            });
        }
    }

    // Método para enviar archivo Excel al backend
    async sendExcelToBackend() {
        const fileInput = document.getElementById('excelFileInput');
        const sendBtn = document.getElementById('sendTestBtn');
        const responseArea = document.getElementById('testResponseArea');
        const errorArea = document.getElementById('testErrorArea');
        const responseContent = document.getElementById('testResponseContent');
        const errorContent = document.getElementById('testErrorContent');

        if (!fileInput || !sendBtn) return;

        const file = fileInput.files[0];
        
        if (!file) {
            Utils.showNotification('Por favor, selecciona un archivo Excel', 'warning');
            return;
        }

        try {
            // Mostrar estado de carga
            sendBtn.classList.add('is-loading');
            sendBtn.disabled = true;
            
            // Ocultar áreas de respuesta y error anteriores
            responseArea.style.display = 'none';
            errorArea.style.display = 'none';

            // Crear FormData para enviar el archivo
            const formData = new FormData();
            formData.append('file', file);
            formData.append('timestamp', new Date().toISOString());
            formData.append('source', 'tuya-frontend');

            // Realizar petición POST al backend
            const response = await fetch('http://localhost:8000/test', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Mostrar respuesta exitosa
            responseContent.innerHTML = `
                <div class="has-text-success">
                    <i class="fas fa-check-circle"></i>
                    <strong>Archivo Excel enviado exitosamente:</strong>
                </div>
                <div class="mt-2">
                    <p><strong>Archivo:</strong> ${file.name}</p>
                    <p><strong>Tamaño:</strong> ${(file.size / 1024).toFixed(2)} KB</p>
                    <p><strong>Tipo:</strong> ${file.type || 'No especificado'}</p>
                </div>
                <div class="mt-3">
                    <strong>Respuesta del backend:</strong>
                    <pre class="mt-2">${JSON.stringify(data, null, 2)}</pre>
                </div>
            `;
            responseArea.style.display = 'block';
            
            Utils.showNotification('Archivo Excel enviado exitosamente al backend', 'success');

        } catch (error) {
            console.error('Error enviando archivo al backend:', error);
            
            // Mostrar error
            errorContent.innerHTML = `
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Error al enviar archivo al backend:</strong><br>
                ${error.message}
            `;
            errorArea.style.display = 'block';
            
            Utils.showNotification('Error al enviar archivo al backend', 'danger');

        } finally {
            // Restaurar estado del botón
            sendBtn.classList.remove('is-loading');
            sendBtn.disabled = false;
        }
    }
} 