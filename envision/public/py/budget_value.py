import frappe

@frappe.whitelist()
def get_budget_value(name):
    doc = frappe.get_doc("Supplier Quotation", name)
    
    budget_sum = 0
    budget_remaining = 0

    # Fetch all budget items for this quotation in one query
    project_budgets = {}
    
    if doc.project:
        
        budget_name = frappe.db.get_value("Project Budget", {
            'company': doc.company,
            'project': doc.project,
            'department': doc.custom_department,
            'workflow_state': "Approved"
        }, 'name')
        
        if budget_name:
            # Fetch budget items only once per budget name
            if budget_name not in project_budgets:
                project_budgets[budget_name] = frappe.db.get_all(
                    "Budget Items",
                    filters={'parent': budget_name},
                    fields=['item', 'current_budget', 'amount']
                )

            for budget in project_budgets[budget_name]:
                if budget['item'] == item.item_group or budget['item'] == item.item_code:
                    budget_sum += budget['amount'] or 0
                    budget_remaining += budget['current_budget'] or 0

    # Assign the calculated values to the custom fields
    else:
       for item in doc.items:
        budget_name = frappe.db.get_value("Project Budget", {
            'company': doc.company,
            'project': item.project,
            'department': doc.custom_department,
            'workflow_state': "Approved"
        }, 'name')
        
        if budget_name:
            # Fetch budget items only once per budget name
            if budget_name not in project_budgets:
                project_budgets[budget_name] = frappe.db.get_all(
                    "Budget Items",
                    filters={'parent': budget_name},
                    fields=['item', 'current_budget', 'amount']
                )

            for budget in project_budgets[budget_name]:
                if budget['item'] == item.item_group or budget['item'] == item.item_code:
                    budget_sum += budget['amount'] or 0
                    budget_remaining += budget['current_budget'] or 0

    # Assign the calculated values to the custom fields
    doc.custom_total_budget = budget_sum
    doc.custom_remaining_budget = budget_remaining
    doc.save()  # Save the document with updated values

    # Return the values to display them on the form
    return {
        "total_budget": budget_sum,
        "remaining_budget": budget_remaining
    }
