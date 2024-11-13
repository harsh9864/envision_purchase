frappe.ui.form.on("Request for Quotation",{
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