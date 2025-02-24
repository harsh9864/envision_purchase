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
frappe.ui.form.on("Purchase Order",{
    refresh:function(frm){
        frm.set_query("department",function(){
            return{
                filters:{
                    'company':frm.doc.company
                }
            }
        })
        frm.set_query("custom_general_terms",function(){
            return{
                filters:{
                    'buying':1,
                    'custom_general':1
                }
            }
        })
    },
    custom_general_terms: function(frm) {
        erpnext.utils.get_terms(cur_frm.doc.custom_general_terms, frm.doc, function(r) {
            if (!r.exc) {
                frappe.model.set_value(frm.doctype, frm.docname, "custom_general_terms_and_condition", r.message);
            }
        });
    }
})