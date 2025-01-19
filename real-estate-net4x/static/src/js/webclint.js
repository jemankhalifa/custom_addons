/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class CRMDashboard extends Component {
    static template = "real-estate-net4x.crm_dashboard_template";
}

registry.category("actions").add("real-estate-net4x.crm_dashboard", CRMDashboard);
