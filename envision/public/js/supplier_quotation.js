frappe.ui.form.on("Supplier Quotation",{
    refresh:function(frm){
        frm.set_query("department",function(){
            return{
                filters:{
                    'company':frm.doc.company
                }
            }
        })
    }
})



frappe.ui.form.on('Supplier Quotation', {
	after_workflow_action: (frm) => {
    if(frm.doc.workflow_state === 'Submitted'){
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Supplier Quotation",
                filters: {
                    'name': ['!=', frm.doc.name],  // Exclude the current record
                    'custom_request_for_quotation': frm.doc.custom_request_for_quotation,
                    'workflow_state' : "Draft"
                }
            },
            callback: function(r) {
                if (r.message && r.message.length > 0) {
                    // Loop through the list of Supplier Quotation records
                    var len = r.message.length;
                    for (var i = 0; i < len; i++) {
                        var doc = r.message[i]; // Get each Supplier Quotation document

                        // Use frappe.db.set_value to update a specific field (replace 'field_name' with actual field)
                        frappe.db.set_value("Supplier Quotation", doc.name, "workflow_state", "Disqualify")
                            .then(r => {
                                console.log(`Updated Supplier Quotation ${doc.name}`);
                            })
                            
                    }
                }
            }
        });
    } 
     
    
	}
});

