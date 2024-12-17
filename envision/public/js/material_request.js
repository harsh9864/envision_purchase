frappe.ui.form.on("Material Request",{
    refresh:function(frm){
        frm.set_query("department",function(){
            return{
                filters:{
                    'company':frm.doc.company
                }
            }
        })
        frm.add_custom_button(__('Cost Estimation'), function() {
            let dialog = new frappe.ui.form.MultiSelectDialog({
                doctype: "Cost Estimation",
                target: frm,
                setters: {
                    department: frm.doc.custom_department // Pre-fill department filter
                },
                add_filters_group: 1, // Allow adding custom filters
                columns: ["name", "opportunity", "department", "total_cost"], // Add more details
                action(selections) {
                    if (!selections.length) {
                        frappe.msgprint(__('Please select at least one Cost Estimation.'));
                        return;
                    }

                    console.log("Selected Cost Estimations:", selections);

                    // Hide the dialog
                    dialog.dialog.hide();

                    // Fetch data for each selected Cost Estimation
                    let all_items = [];
                    let promises = selections.map(ce => {
                        return new Promise((resolve, reject) => {
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Cost Estimation",
                                    name: ce
                                },
                                callback: function(response) {
                                    if (response.message && response.message.cost_estimation_expense) {
                                        resolve(response.message.cost_estimation_expense);
                                    } else {
                                        resolve([]); // Resolve with empty array if no items
                                    }
                                },
                                error: reject
                            });
                        });
                    });

                    // Process all fetched data
                    Promise.all(promises).then(results => {
                        results.forEach(items => {
                            all_items = all_items.concat(items);
                        });

                        // Group items by item_code
                        let grouped_items = {};
                        all_items.forEach(item => {
                            if (item.item_code) {
                                let key = item.item_code;
                                if (!grouped_items[key]) {
                                    grouped_items[key] = {
                                        item_code: item.item_code,
                                        quantity: 0
                                    };
                                }
                                grouped_items[key].quantity += parseFloat(item.quantity) || 0;
                            }
                        });

                        console.log("Grouped Items:", grouped_items);

                        // Batch fetch stock_uom for grouped items
                        let item_codes = Object.keys(grouped_items);
                        frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Item",
                                filters: { item_code: ["in", item_codes] },
                                fields: ["item_code", "stock_uom"]
                            },
                            callback: function(response) {
                                let item_data = response.message || [];
                                let item_map = {};
                                item_data.forEach(item => {
                                    item_map[item.item_code] = item.stock_uom;
                                });

                                // Add items to the child table
                                frm.clear_table("items");
                                Object.values(grouped_items).forEach(item => {
                                    frm.add_child("items", {
                                        item_code: item.item_code,
                                        qty: item.quantity,
                                        uom: item_map[item.item_code] || "",
                                        conversion_factor:1
                                    });
                                });

                                frm.refresh_field("items");

                                frappe.msgprint({
                                    title: __('Success'),
                                    message: __('Grouped items have been added to the child table.'),
                                    indicator: 'green'
                                });
                            }
                        });
                    }).catch(error => {
                        frappe.msgprint({
                            title: __('Error'),
                            message: __('Failed to fetch items. Please try again.'),
                            indicator: 'red'
                        });
                        console.error("Error fetching items:", error);
                    });
                }
            });
        }, __("Get Items From"));
    }
})
