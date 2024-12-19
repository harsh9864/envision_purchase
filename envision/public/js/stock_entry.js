frappe.ui.form.on('Stock Entry', {
    project:function(frm) {
        if (frm.doc.project ) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Stock Ledger Entry",
                    filters: {
                        project: frm.doc.project,
                        posting_datetime: ["<=", frappe.datetime.now_datetime()] // Filter entries up to the current date and time
                    },
                    fields: ['item_code', 'actual_qty', 'valuation_rate', 'warehouse', 'posting_datetime'] // Fetch specific fields
                },
                callback: function(r) {
                    if (r.message && r.message.length) {
                        // Group data by item_code
                        let grouped_data = {};
                        let available_item_codes = [];

                        r.message.forEach(entry => {
                            const item_code = entry.item_code;

                            if (!grouped_data[item_code]) {
                                grouped_data[item_code] = {
                                    item_code: item_code,
                                    net_qty: 0,
                                    total_valuation: 0,
                                    warehouses: [],
                                    posting_datetime: entry.posting_datetime
                                };
                            }

                            // Calculate net quantity
                            grouped_data[item_code].net_qty += entry.actual_qty;
                            grouped_data[item_code].total_valuation += entry.actual_qty * entry.valuation_rate;

                            if (!grouped_data[item_code].warehouses.includes(entry.warehouse)) {
                                grouped_data[item_code].warehouses.push(entry.warehouse);
                            }
                        });

                        // Filter items with net stock greater than 0 and collect item codes
                        let available_items = Object.values(grouped_data).filter(group => group.net_qty > 0);
                        available_items.forEach(group => {
                            available_item_codes.push(group.item_code); // Collect item codes
                        });

                        console.log("Available Item Codes:", available_item_codes);

                        // Apply filter to child table
                        frm.fields_dict['items'].grid.get_field('item_code').get_query = function() {
                            return {
                                filters: {
                                    item_code: ["in", available_item_codes]
                                }
                            };
                        };

                       
                    } else {
                        frappe.msgprint({
                            title: __('No Data'),
                            message: __('No Stock Ledger Entries found for the selected criteria.'),
                            indicator: 'orange'
                        });
                    }
                },
                error: function(err) {
                    console.error("Error fetching Stock Ledger Entries:", err);
                }
            });
        }
    }
});
