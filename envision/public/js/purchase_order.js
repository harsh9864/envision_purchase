frappe.ui.form.on('Purchase Order Item', {
    item_code: function(frm, cdt, cdn) {
        $.each(frm.doc.items || [], function(i, d) {
           frappe.call({
               method:"frappe.client.get",
               args:{
                   doctype:"Item",
                   'name':d.item_code,
                   field:["*"]
               },
               callback:function(r){
                   if(r.message.custom_is_brand == 1){
                       cur_frm.fields_dict.items.grid.toggle_reqd
    ("brand", 1)
    frm.fields_dict.items.grid.update_docfield_property('brand', "read_only", 0);
    frm.fields_dict.items.grid.update_docfield_property('brand', "hidden", 0);
  
                   }
               }
           })
        });
    }
});
