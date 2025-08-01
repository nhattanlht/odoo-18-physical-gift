/** @odoo-module **/

import { ListView } from "@web/views/list/list_view";
import { listView } from "@web/views/list/list_view_registry";
import { patch } from "@web/core/utils/patch";

// Patch the ListView to add custom functionality
patch(ListView.prototype, {
    setup() {
        super.setup();
        this.setupPhysicalGiftFeatures();
    },

    setupPhysicalGiftFeatures() {
        // Add custom event listeners for Physical Gift specific features
        if (this.props.resModel === 'physical.gift.program') {
            this.setupFilterButtons();
            this.setupExportFunctionality();
        }
    },

    setupFilterButtons() {
        // Custom filter button functionality
        const filterButtons = document.querySelectorAll('.btn-filter');
        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleFilter();
            });
        });
    },

    setupExportFunctionality() {
        // Custom export functionality
        const exportButtons = document.querySelectorAll('.btn-export');
        exportButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleExport();
            });
        });
    },

    async handleFilter() {
        // Custom filter logic
        console.log('Filtering Physical Gift programs...');
        // Add your custom filter logic here
    },

    async handleExport() {
        // Custom export logic
        console.log('Exporting Physical Gift programs...');
        // Add your custom export logic here
        try {
            // Example export functionality
            const records = await this.model.root.records;
            const data = records.map(record => ({
                id: record.data.id,
                name: record.data.name,
                company: record.data.company_id[1],
                creator: record.data.creator_id[1],
                state: record.data.state
            }));
            
            // Create CSV content
            const csvContent = this.convertToCSV(data);
            this.downloadCSV(csvContent, 'physical_gift_programs.csv');
        } catch (error) {
            console.error('Export failed:', error);
        }
    },

    convertToCSV(data) {
        const headers = ['ID', 'Tên chương trình', 'Công ty', 'Người tạo', 'Trạng thái'];
        const csvRows = [headers.join(',')];
        
        data.forEach(row => {
            const values = [
                row.id,
                `"${row.name}"`,
                `"${row.company}"`,
                `"${row.creator}"`,
                row.state
            ];
            csvRows.push(values.join(','));
        });
        
        return csvRows.join('\n');
    },

    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
});

// Custom component for Physical Gift specific features
export class PhysicalGiftListView extends ListView {
    setup() {
        super.setup();
        this.setupCustomFeatures();
    }

    setupCustomFeatures() {
        // Add any additional custom features specific to Physical Gift
        this.setupProgramStatusUpdates();
    }

    setupProgramStatusUpdates() {
        // Handle program status updates
        const updateButtons = document.querySelectorAll('[name="action_activate"], [name="action_deactivate"], [name="action_close"]');
        updateButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleStatusUpdate(button.name);
            });
        });
    }

    async handleStatusUpdate(action) {
        // Handle status update actions
        console.log(`Updating program status with action: ${action}`);
        // Add your custom status update logic here
    }
}

// Register the custom list view
listView.add('physical_gift_program_list', PhysicalGiftListView); 