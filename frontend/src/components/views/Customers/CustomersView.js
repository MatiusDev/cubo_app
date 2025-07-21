// Vista de Clientes
export const getCustomersContent = () => {
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
};

export const initializeCustomersView = () => {
    // Inicializar funcionalidades específicas de la vista de Clientes
    console.log('Vista de Clientes inicializada');
};

export const CustomersView = {
    getContent: getCustomersContent,
    initialize: initializeCustomersView
}; 