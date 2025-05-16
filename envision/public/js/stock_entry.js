// frappe.ui.form.on('Stock Entry', {
//     project:function(frm) {
//         if (frm.doc.project ) {
//             frappe.call({
//                 method: "frappe.client.get_list",
//                 args: {
//                     doctype: "Stock Ledger Entry",
//                     filters: {
//                         project: frm.doc.project,
//                         posting_datetime: ["<=", frappe.datetime.now_datetime()] // Filter entries up to the current date and time
//                     },
//                     fields: ['item_code', 'actual_qty', 'valuation_rate', 'warehouse', 'posting_datetime'] // Fetch specific fields
//                 },
//                 callback: function(r) {
//                     if (r.message && r.message.length) {
//                         // Group data by item_code
//                         let grouped_data = {};
//                         let available_item_codes = [];

//                         r.message.forEach(entry => {
//                             const item_code = entry.item_code;

//                             if (!grouped_data[item_code]) {
//                                 grouped_data[item_code] = {
//                                     item_code: item_code,
//                                     net_qty: 0,
//                                     total_valuation: 0,
//                                     warehouses: [],
//                                     posting_datetime: entry.posting_datetime
//                                 };
//                             }

//                             // Calculate net quantity
//                             grouped_data[item_code].net_qty += entry.actual_qty;
//                             grouped_data[item_code].total_valuation += entry.actual_qty * entry.valuation_rate;

//                             if (!grouped_data[item_code].warehouses.includes(entry.warehouse)) {
//                                 grouped_data[item_code].warehouses.push(entry.warehouse);
//                             }
//                         });

//                         // Filter items with net stock greater than 0 and collect item codes
//                         let available_items = Object.values(grouped_data).filter(group => group.net_qty > 0);
//                         available_items.forEach(group => {
//                             available_item_codes.push(group.item_code); // Collect item codes
//                         });

//                         console.log("Available Item Codes:", available_item_codes);

//                         // Apply filter to child table
//                         frm.fields_dict['items'].grid.get_field('item_code').get_query = function() {
//                             return {
//                                 filters: {
//                                     item_code: ["in", available_item_codes]
//                                 }
//                             };
//                         };

                       
//                     }
//                 },
//                 error: function(err) {
//                     console.error("Error fetching Stock Ledger Entries:", err);
//                 }
//             });
//         }
//     }
// });

frappe.ui.form.on('Stock Entry', {
    project: function(frm) {
        if (frm.doc.project) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Stock Ledger Entry",
                    filters: {
                        project: frm.doc.project,
                        posting_datetime: ["<=", frappe.datetime.now_datetime()]
                    },
                    fields: ['item_code', 'actual_qty', 'valuation_rate', 'warehouse', 'posting_datetime','stock_uom']
                },
                callback: function(r) {
                    if (r.message && r.message.length) {
                        let grouped_data = {};
                        let available_item_codes = [];

                        r.message.forEach(entry => {
                            const key = `${entry.item_code}||${entry.warehouse}`;
                            if (!grouped_data[key]) {
                                grouped_data[key] = {
                                    item_code: entry.item_code,
                                    warehouse: entry.warehouse,
                                    net_qty: 0,
                                    uom : entry.stock_uom,

                                };
                            }

                            grouped_data[key].net_qty += entry.actual_qty;
                        });

                        // Clear child table
                        frm.clear_table("items");

                        Object.values(grouped_data).forEach(group => {
                            if (group.net_qty > 0) {
                                available_item_codes.push(group.item_code);

                                let row = frm.add_child("items");
                                row.item_code = group.item_code;
                                row.qty = group.net_qty;
                                row.s_warehouse = group.warehouse; 
                                row.stock_uom = group.uom; // Set stock_uom
                                row.conversion_factor = 1;
                                row.transfer_qty = group.net_qty * row.conversion_factor // Set conversion factor to 1
                                // Set target warehouse
                            }
                        });

                        frm.refresh_field("items");

                        // Restrict item_code selection in child table
                        frm.fields_dict['items'].grid.get_field('item_code').get_query = function() {
                            return {
                                filters: {
                                    item_code: ["in", [...new Set(available_item_codes)]]
                                }
                            };
                        };
                    }
                },
                error: function(err) {
                    console.error("Error fetching Stock Ledger Entries:", err);
                }
            });
        }
    }
});

frappe.ui.form.on('Stock Entry', {
    refresh:function(frm) {
        if(frm.doc.stock_entry_type == "Sale Delivery"){
            frm.set_query("custom_sales_order", function() {
                return {
                    "filters": {
                        "project":frm.doc.project,
                        "docstatus": 1,
                    }
                }
            })
            frm.set_df_property("custom_sales_order", "reqd", 1);
            frm.set_query("custom_sales_invoice", function() {
                return {
                    "filters": {
                        "project":frm.doc.project
                    }
                }
            })
        }
        
    }
})