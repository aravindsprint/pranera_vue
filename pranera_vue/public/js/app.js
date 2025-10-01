// pranera_vue/public/js/app.js

import { createApp } from 'vue'
import SalesOrderReport from './components/SalesOrderReport.vue'

// Initialize Vue app
const app = createApp({})

// Register components
app.component('sales-order-report', SalesOrderReport)

// Mount the app
app.mount('#vue-app')

console.log('Vue app initialized')