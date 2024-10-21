frappe.ui.form.on('Purchase Receipt Item', {
    item_code: function(frm) {
        frm.doc.items.forEach(function(d) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Item",
                    name: d.item_code
                },
                callback: function(r) {
                    if (r.message) {
                       
                        if(r.message.is_stock_item == 1){
                              // To hide the field based on some condition
                        frm.fields_dict["items"].grid.update_docfield_property(
                            "custom_material_code", "hidden", 1
                        );
                        }
                          if(r.message.custom_is_brand == 1){
                       cur_frm.fields_dict.items.grid.toggle_reqd
    ("brand", 1)
    frm.fields_dict.items.grid.update_docfield_property('brand', "read_only", 0);
    frm.fields_dict.items.grid.update_docfield_property('brand', "hidden", 0);
  
                   }
                      
                    }
                }
            });
        });
    }
});

