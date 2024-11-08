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
            // Check if `custom_request_for_quotation` is populated
            // console.log("Custom RFQ value: ", doc.custom_request_for_quotation);
            
            // Ensure custom_request_for_quotation exists before proceeding
            // if (!doc.custom_request_for_quotation) {
            //     frappe.msgprint(__('No Request for Quotation found for this document.'));
                
            //     return;
            // }
            
            // Set route options to filter the report by the custom_request_for_quotation field
            frappe.route_options = {
                request_for_quotation: doc.custom_request_for_quotation
            };
            
            // Route to the "Supplier Comparison" report with the applied filters
            frappe.set_route("query-report", "Comparison");
        }
    }
};
