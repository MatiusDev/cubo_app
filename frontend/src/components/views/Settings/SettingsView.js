// Vista de Configuración
export const getSettingsContent = () => {
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
};

export const initializeSettingsView = () => {
    // Inicializar funcionalidades específicas de la vista de Configuración
    console.log('Vista de Configuración inicializada');
};

export const SettingsView = {
    getContent: getSettingsContent,
    initialize: initializeSettingsView
}; 