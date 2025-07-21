// Exportar todas las vistas
export { BalancesView } from './Balances/BalancesView.js'
export { SalesView } from './Sales/SalesView.js'
export { InventoryView } from './Inventory/InventoryView.js'
export { CustomersView } from './Customers/CustomersView.js'
export { ReportsView } from './Reports/ReportsView.js'
export { TestView } from './Test/TestView.js'
export { SettingsView } from './Settings/SettingsView.js'
export { DefaultView } from './Default/DefaultView.js'
// Las siguientes vistas deben importarse desde src/views si existen
// export { HomeView } from '../../views/HomeView.js';
// export { DashboardView } from '../../views/DashboardView.js';
// export { NotFoundView } from '../../views/NotFoundView.js';

// Mapa de vistas por sección
export const VIEWS_MAP = {
    balances: 'BalancesView',
    sales: 'SalesView',
    inventory: 'InventoryView',
    customers: 'CustomersView',
    reports: 'ReportsView',
    test: 'TestView',
    settings: 'SettingsView'
}

// Función para obtener la vista correspondiente
export const getViewForSection = (sectionId) => {
    const viewName = VIEWS_MAP[sectionId]
    if (viewName) {
        return { [viewName]: true }
    }
    return { DefaultView: true }
} 