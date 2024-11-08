frappe.ui.form.on("Sales Order",{
    project:function(frm){
        frappe.call({
            method:"frappe.client.get",
            args:{
                doctype:"Project",
                name:cur_frm.doc.project,
                field:'*'
            },
            callback:function(r){
                console.log(r.message.customer)
                
                frm.set_query("customer",function(){
                    return{
                        filters:{
                            'name': ["in", r.message.customer]
                           
                        }
                        
                    };
                });
            }
        })
    }
})