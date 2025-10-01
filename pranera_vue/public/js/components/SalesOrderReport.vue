<template>
  <div class="sales-order-report">
    <div class="report-header">
      <h2>Sales Order Report</h2>
      <div class="filters">
        <div class="filter-group">
          <label>From Date:</label>
          <input type="date" v-model="filters.from_date" @change="fetchData" />
        </div>
        <div class="filter-group">
          <label>To Date:</label>
          <input type="date" v-model="filters.to_date" @change="fetchData" />
        </div>
        <div class="filter-group">
          <label>Sales Person:</label>
          <input type="text" v-model="filters.sales_person" @change="fetchData" />
        </div>
        <div class="filter-group">
          <button @click="fetchData" class="btn btn-primary">Refresh</button>
          <button @click="exportToCSV" class="btn btn-secondary">Export CSV</button>
        </div>
      </div>
    </div>

    <div class="report-summary" v-if="summary">
      <div class="summary-card">
        <h4>Total Orders</h4>
        <span class="summary-value">{{ summary.totalOrders }}</span>
      </div>
      <div class="summary-card">
        <h4>Total Amount</h4>
        <span class="summary-value">{{ formatCurrency(summary.totalAmount) }}</span>
      </div>
      <div class="summary-card">
        <h4>Pending Amount</h4>
        <span class="summary-value">{{ formatCurrency(summary.pendingAmount) }}</span>
      </div>
      <div class="summary-card">
        <h4>Delivered Amount</h4>
        <span class="summary-value">{{ formatCurrency(summary.deliveredAmount) }}</span>
      </div>
    </div>

    <div class="table-container">
      <table class="sales-order-table">
        <thead>
          <tr>
            <th @click="sortBy('posting_date')" class="sortable">
              Date 
              <span v-if="sortField === 'posting_date'" class="sort-icon">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th @click="sortBy('delivery_date')" class="sortable">
              Delivery Date
              <span v-if="sortField === 'delivery_date'" class="sort-icon">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th>Sales Order</th>
            <th>Item Code</th>
            <th>Commercial Name</th>
            <th>Color</th>
            <th>Width</th>
            <th @click="sortBy('qty')" class="sortable">
              Qty
              <span v-if="sortField === 'qty'" class="sort-icon">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th>Delivered Qty</th>
            <th>Pending Qty</th>
            <th @click="sortBy('original_amount')" class="sortable">
              Amount
              <span v-if="sortField === 'original_amount'" class="sort-icon">
                {{ sortOrder === 1 ? '↑' : '↓' }}
              </span>
            </th>
            <th>Item Status</th>
            <th>UOM</th>
            <th>Customer</th>
            <th>Sales Person</th>
            <th>Document Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedData" :key="item.name + '-' + item.item_code" 
              :class="getRowClass(item)">
            <td>{{ formatDate(item.posting_date) }}</td>
            <td>{{ formatDate(item.delivery_date) }}</td>
            <td class="sales-order-link">{{ item.name }}</td>
            <td>{{ item.item_code }}</td>
            <td>{{ item.commercial_name || '-' }}</td>
            <td>{{ item.color || '-' }}</td>
            <td>{{ item.width || '-' }}</td>
            <td class="number">{{ formatNumber(item.qty) }}</td>
            <td class="number">{{ formatNumber(item.delivered_qty) }}</td>
            <td class="number">{{ formatNumber(item.pending_qty) }}</td>
            <td class="number">{{ formatCurrency(item.original_amount) }}</td>
            <td>
              <span class="status-badge" :class="getStatusClass(item.custom_item_status)">
                {{ item.custom_item_status || 'Not Set' }}
              </span>
            </td>
            <td>{{ item.stock_uom }}</td>
            <td>{{ item.customer }}</td>
            <td>{{ item.sales_person || '-' }}</td>
            <td>
              <span class="status-badge" :class="getDocStatusClass(item.status)">
                {{ item.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        Loading data...
      </div>

      <div v-if="!loading && data.length === 0" class="no-data">
        No sales order data found.
      </div>
    </div>

    <div class="pagination" v-if="data.length > 0">
      <div class="pagination-info">
        Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ data.length }} entries
      </div>
      <div class="pagination-controls">
        <button @click="previousPage" :disabled="currentPage === 1" class="btn btn-sm">
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="btn btn-sm">
          Next
        </button>
      </div>
      <div class="page-size">
        <label>Show:</label>
        <select v-model="pageSize" @change="resetPagination">
          <option value="10">10</option>
          <option value="25">25</option>
          <option value="50">50</option>
          <option value="100">100</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SalesOrderReport',
  data() {
    return {
      data: [],
      loading: false,
      error: null,
      filters: {
        from_date: '',
        to_date: '',
        sales_person: '',
        item_code: '',
        commercial_name: '',
        color: '',
        custom_item_status: '',
        delivery_status: '',
        series: ''
      },
      sortField: 'posting_date',
      sortOrder: -1, // -1 for descending, 1 for ascending
      currentPage: 1,
      pageSize: 25
    }
  },
  computed: {
    sortedData() {
      const sorted = [...this.data];
      sorted.sort((a, b) => {
        let aValue = a[this.sortField];
        let bValue = b[this.sortField];
        
        // Handle null/undefined values
        if (aValue == null) aValue = '';
        if (bValue == null) bValue = '';
        
        // Handle numeric sorting
        if (typeof aValue === 'number' && typeof bValue === 'number') {
          return this.sortOrder === 1 ? aValue - bValue : bValue - aValue;
        }
        
        // Handle date sorting
        if (this.sortField.includes('date')) {
          aValue = new Date(aValue);
          bValue = new Date(bValue);
          return this.sortOrder === 1 ? aValue - bValue : bValue - aValue;
        }
        
        // String sorting
        return this.sortOrder === 1 
          ? aValue.toString().localeCompare(bValue.toString())
          : bValue.toString().localeCompare(aValue.toString());
      });
      return sorted;
    },
    
    paginatedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.sortedData.slice(start, end);
    },
    
    totalPages() {
      return Math.ceil(this.data.length / this.pageSize);
    },
    
    startIndex() {
      return (this.currentPage - 1) * this.pageSize;
    },
    
    endIndex() {
      const end = this.startIndex + this.pageSize;
      return end > this.data.length ? this.data.length : end;
    },
    
    summary() {
      if (this.data.length === 0) return null;
      
      return {
        totalOrders: new Set(this.data.map(item => item.name)).size,
        totalAmount: this.data.reduce((sum, item) => sum + (item.original_amount || 0), 0),
        pendingAmount: this.data.reduce((sum, item) => sum + (item.pending_amount || 0), 0),
        deliveredAmount: this.data.reduce((sum, item) => sum + (item.delivered_amount || 0), 0)
      };
    }
  },
  mounted() {
    this.fetchData();
    // Set default date range to last 30 days
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    this.filters.from_date = thirtyDaysAgo.toISOString().split('T')[0];
    this.filters.to_date = new Date().toISOString().split('T')[0];
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      
      try {
        // Clean filters - remove empty values
        const cleanFilters = Object.fromEntries(
          Object.entries(this.filters).filter(([_, value]) => value !== '')
        );
        
        const response = await fetch('/api/method/pranera_vue.pranera_vue.api.sales_order_api.get_sales_order_report', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Frappe-CSRF-Token': this.getCSRFToken()
          },
          body: JSON.stringify({
            filters: cleanFilters
          })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.message && result.message.message) {
          this.data = result.message.message;
        } else {
          this.data = [];
        }
        
        this.currentPage = 1; // Reset to first page on new data
      } catch (error) {
        console.error('Error fetching sales order data:', error);
        this.error = 'Failed to fetch sales order data. Please try again.';
        this.data = [];
      } finally {
        this.loading = false;
      }
    },
    
    getCSRFToken() {
      // Frappe usually stores CSRF token in meta tag
      return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    },
    
    sortBy(field) {
      if (this.sortField === field) {
        this.sortOrder = -this.sortOrder;
      } else {
        this.sortField = field;
        this.sortOrder = -1; // Default to descending for new fields
      }
    },
    
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    
    resetPagination() {
      this.currentPage = 1;
    },
    
    formatDate(dateString) {
      if (!dateString) return '-';
      return new Date(dateString).toLocaleDateString();
    },
    
    formatNumber(value) {
      if (value == null) return '-';
      return new Intl.NumberFormat().format(value);
    },
    
    formatCurrency(value) {
      if (value == null) return '-';
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
      }).format(value);
    },
    
    getRowClass(item) {
      if (item.custom_item_status === 'Cancelled') {
        return 'cancelled-row';
      }
      if (item.pending_qty === 0) {
        return 'completed-row';
      }
      return '';
    },
    
    getStatusClass(status) {
      const statusMap = {
        'Completed': 'status-completed',
        'Cancelled': 'status-cancelled',
        'In Progress': 'status-in-progress',
        'Not Set': 'status-not-set'
      };
      return statusMap[status] || 'status-not-set';
    },
    
    getDocStatusClass(status) {
      const statusMap = {
        'Completed': 'status-completed',
        'To Deliver and Bill': 'status-pending',
        'Draft': 'status-draft'
      };
      return statusMap[status] || 'status-not-set';
    },
    
    exportToCSV() {
      const headers = [
        'Date', 'Delivery Date', 'Sales Order', 'Item Code', 'Commercial Name',
        'Color', 'Width', 'Qty', 'Delivered Qty', 'Pending Qty', 'Amount',
        'Item Status', 'UOM', 'Customer', 'Sales Person', 'Document Status'
      ];
      
      const csvData = this.sortedData.map(item => [
        this.formatDate(item.posting_date),
        this.formatDate(item.delivery_date),
        item.name,
        item.item_code,
        item.commercial_name || '',
        item.color || '',
        item.width || '',
        item.qty,
        item.delivered_qty,
        item.pending_qty,
        item.original_amount,
        item.custom_item_status || '',
        item.stock_uom,
        item.customer,
        item.sales_person || '',
        item.status
      ]);
      
      const csvContent = [
        headers.join(','),
        ...csvData.map(row => row.map(field => `"${field}"`).join(','))
      ].join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sales-order-report-${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    }
  }
}
</script>

<style scoped>
.sales-order-report {
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.report-header {
  margin-bottom: 20px;
}

.report-header h2 {
  color: #2e3338;
  margin-bottom: 15px;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: 500;
  font-size: 12px;
  color: #6c7680;
}

.filter-group input,
.filter-group select {
  padding: 6px 8px;
  border: 1px solid #d1d8dd;
  border-radius: 3px;
  font-size: 13px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
}

.btn-primary {
  background-color: #2490ef;
  color: white;
}

.btn-secondary {
  background-color: #6c7680;
  color: white;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.report-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.summary-card {
  background: white;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #d1d8dd;
  text-align: center;
}

.summary-card h4 {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #6c7680;
  text-transform: uppercase;
}

.summary-value {
  font-size: 18px;
  font-weight: 600;
  color: #2e3338;
}

.table-container {
  background: white;
  border: 1px solid #d1d8dd;
  border-radius: 4px;
  overflow: hidden;
}

.sales-order-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.sales-order-table th {
  background-color: #f5f7fa;
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  color: #2e3338;
  border-bottom: 1px solid #d1d8dd;
  cursor: pointer;
  user-select: none;
}

.sales-order-table th.sortable:hover {
  background-color: #ebeff4;
}

.sort-icon {
  margin-left: 4px;
  font-weight: bold;
}

.sales-order-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #f0f4f7;
  vertical-align: top;
}

.sales-order-table tr:last-child td {
  border-bottom: none;
}

.sales-order-table tr:hover {
  background-color: #fafbfc;
}

.cancelled-row {
  background-color: #fff4f4 !important;
  color: #e53935;
}

.completed-row {
  background-color: #f4fff4 !important;
}

.number {
  text-align: right;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.sales-order-link {
  color: #2490ef;
  font-weight: 500;
}

.status-badge {
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
}

.status-completed {
  background-color: #e3fcef;
  color: #00875a;
}

.status-cancelled {
  background-color: #ffeaea;
  color: #de3618;
}

.status-pending {
  background-color: #fff8e6;
  color: #ff8b00;
}

.status-draft {
  background-color: #f4f5f7;
  color: #6c7680;
}

.status-not-set {
  background-color: #f4f5f7;
  color: #6c7680;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #6c7680;
}

.spinner {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #2490ef;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-data {
  padding: 40px;
  text-align: center;
  color: #6c7680;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  font-size: 13px;
}

.pagination-info {
  color: #6c7680;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-info {
  margin: 0 10px;
  color: #2e3338;
}

.page-size {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-size select {
  padding: 4px;
  border: 1px solid #d1d8dd;
  border-radius: 3px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .report-summary {
    grid-template-columns: 1fr;
  }
  
  .pagination {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .sales-order-table {
    min-width: 1000px;
  }
}
</style>