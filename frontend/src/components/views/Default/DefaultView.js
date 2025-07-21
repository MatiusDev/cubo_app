// Vista por defecto para secciones no implementadas
export const getDefaultContent = (sectionId) => {
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
};

export const initializeDefaultView = (sectionId) => {
    // Inicializar funcionalidades específicas de la vista por defecto
    console.log(`Vista por defecto inicializada para sección: ${sectionId}`);
};

export const DefaultView = {
    getContent: getDefaultContent,
    initialize: initializeDefaultView
}; 