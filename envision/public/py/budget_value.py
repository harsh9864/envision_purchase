import frappe

@frappe.whitelist()
def get_budget_value(name):
    doc = frappe.get_doc("Supplier Quotation", name)
    
    budget_sum = 0
    budget_remaining = 0

    project_budgets = {}
    used_budget_keys = set()  # To prevent duplicate counting

    # Check and calculate budget based on project
    if doc.project:
        budget_name = frappe.db.get_value("Project Budget", {
            'company': doc.company,
            'project': doc.project,
            'department': doc.custom_department,
            'workflow_state': "Approved"
        }, 'name')
        
        if budget_name:
            if budget_name not in project_budgets:
                project_budgets[budget_name] = frappe.db.get_all(
                    "Budget Items",
                    filters={'parent': budget_name},
                    fields=['item', 'current_budget', 'amount']
                )

            for item in doc.items:
                for budget in project_budgets[budget_name]:
                    budget_key = budget['item']
                    if (budget_key == item.item_group or budget_key == item.item_code) and budget_key not in used_budget_keys:
                        budget_sum += budget['amount'] or 0
                        budget_remaining += budget['current_budget'] or 0
                        used_budget_keys.add(budget_key)
    else:
        for item in doc.items:
            budget_name = frappe.db.get_value("Project Budget", {
                'company': doc.company,
                'project': item.project,
                'department': doc.custom_department,
                'workflow_state': "Approved"
            }, 'name')
            
            if budget_name:
                if budget_name not in project_budgets:
                    project_budgets[budget_name] = frappe.db.get_all(
                        "Budget Items",
                        filters={'parent': budget_name},
                        fields=['item', 'current_budget', 'amount']
                    )

                for budget in project_budgets[budget_name]:
                    budget_key = budget['item']
                    if (budget_key == item.item_group or budget_key == item.item_code) and budget_key not in used_budget_keys:
                        budget_sum += budget['amount'] or 0
                        budget_remaining += budget['current_budget'] or 0
                        used_budget_keys.add(budget_key)

    # Assign the calculated values to the custom fields
    doc.custom_total_budget = budget_sum
    doc.custom_remaining_budget = budget_remaining
    doc.save()

    return {
        "total_budget": budget_sum,
        "remaining_budget": budget_remaining
    }
