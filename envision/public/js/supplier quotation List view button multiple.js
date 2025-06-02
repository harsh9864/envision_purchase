frappe.listview_settings['Supplier Quotation'] = {
    button: {
        show: function(doc) {
            return true;  // Always show the button
        },
        get_label: function() {
            return __('Comparison');  // Label for the button
        },
        get_description: function(doc) {
            return __('Print {0}', [doc.name]);  // Tooltip text
        },
        action: function(doc) {
         
            frappe.route_options = {
                request_for_quotation: doc.custom_request_for_quotation
            };
            
            // Route to the "Supplier Comparison" report with the applied filters
            frappe.set_route("query-report", "Comparison");
        }
    }
};
