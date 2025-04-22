import frappe

@frappe.whitelist()
def get_budget_value(name):
    doc = frappe.get_doc("Supplier Quotation", name)

    budget_sum = 0
    budget_remaining = 0

    project_budgets = {}   # Cache budgets already fetched
    used_budget_keys = set()
    fiscal_year_result = frappe.db.sql("""
        SELECT fy.name
        FROM `tabFiscal Year` fy
        JOIN `tabFiscal Year Company` fyc ON fyc.parent = fy.name
        WHERE
            fyc.company = %(company)s
            AND fy.year_start_date <= %(transaction_date)s
            AND fy.year_end_date >= %(transaction_date)s
        LIMIT 1
    """, {
        "company": doc.company,
        "transaction_date": doc.transaction_date
    }, as_dict=True)

    fiscal_year = fiscal_year_result[0]["name"] if fiscal_year_result else None

    if not fiscal_year:
        frappe.throw(f"No Fiscal Year found for Company {doc.company} and transaction date {doc.transaction_date}")

    # If main project exists (doc.project), first handle that separately
    if doc.project:
        budget_name = frappe.db.get_value("Project Budget", {
            'company': doc.company,
            'project': doc.project,
            'department': doc.custom_department,
            'workflow_state': "Approved",
            'fiscal_year': fiscal_year
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
                    budget_key = (budget_name, budget['item'])  # use tuple to avoid clash across projects
                    if (budget['item'] == item.item_group or budget['item'] == item.item_code) and budget_key not in used_budget_keys:
                        budget_sum += budget['amount'] or 0
                        budget_remaining += budget['current_budget'] or 0
                        used_budget_keys.add(budget_key)

    # Now handle each item separately if no main project or mixed projects
    for item in doc.items:
        if not item.project:
            continue  # Skip if project is missing at item level

        budget_name = frappe.db.get_value("Project Budget", {
            'company': doc.company,
            'project': item.project,
            'department': doc.custom_department,
            'workflow_state': "Approved",
            'fiscal_year': fiscal_year
        }, 'name')

        if not budget_name:
            continue

        if budget_name not in project_budgets:
            project_budgets[budget_name] = frappe.db.get_all(
                "Budget Items",
                filters={'parent': budget_name},
                fields=['item', 'current_budget', 'amount']
            )

        for budget in project_budgets[budget_name]:
            budget_key = (budget_name, budget['item'])  # again tuple (budget, item) to avoid duplicates
            if (budget['item'] == item.item_group or budget['item'] == item.item_code) and budget_key not in used_budget_keys:
                budget_sum += budget['amount'] or 0
                budget_remaining += budget['current_budget'] or 0
                used_budget_keys.add(budget_key)

    # Update custom fields and save
    doc.custom_total_budget = budget_sum
    doc.custom_remaining_budget = budget_remaining
    doc.save()

    return {
        "total_budget": budget_sum,
        "remaining_budget": budget_remaining
    }
