/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class CustomDashboard extends Component {
    constructor() {
        super(...arguments);
    }

    mounted() {
        // Render Pie Chart when the component is mounted
        this.renderPieChart();
    }

    renderPieChart() {
        const ctx = document.getElementById('pieChart').getContext('2d');  // Get canvas element
        new Chart(ctx, {
            type: 'pie',  // Pie chart type
            data: {
                labels: ['Category A', 'Category B', 'Category C'], // Labels for each section
                datasets: [{
                    data: [40, 30, 30], // Values for each category
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe'], // Colors for each section
                    hoverOffset: 4, // Hover effect for sections
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',  // Position of the legend
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw + '%';
                            }
                        }
                    }
                }
            }
        });
    }
}

CustomDashboard.template = "custom_dashboard_template";

registry.category("actions").add("custom_dashboard", CustomDashboard);
