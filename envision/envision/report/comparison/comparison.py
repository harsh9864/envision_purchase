# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from collections import defaultdict
import frappe
from frappe import _
from frappe.utils import flt
import locale

# Set the locale for currency formatting (e.g., US dollars)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
def execute(filters=None):
    if not filters:
        return [], []

    supplier_quotation_data = get_data(filters)

    # Dynamically generate columns based on suppliers
    columns = get_columns(supplier_quotation_data)

    data = prepare_data(supplier_quotation_data)
   
    
    return columns, data

def get_data(filters):
    sq = frappe.qb.DocType("Supplier Quotation")
    sq_item = frappe.qb.DocType("Supplier Quotation Item")

    query = (
        frappe.qb.from_(sq_item)
        .from_(sq)
        .select(
            sq_item.parent,
            sq_item.item_code,
            sq_item.rate,
            sq_item.qty,
            sq_item.amount,
            sq.supplier.as_("supplier_code"),
            sq.supplier_name.as_("supplier_name"),
            sq.name,
            sq.custom_remarks,
            sq.incoterm,
            sq.named_place,
            sq.custom_payment_terms,
            sq.custom_delivery_terms,
            sq_item.request_for_quotation_item
        )
        .where(
            (sq_item.parent == sq.name)
            & (sq_item.docstatus < 2)
            & (sq.company == filters.get("company"))
            & (sq.transaction_date.between(filters.get("from_date"), filters.get("to_date")))
        )
          .groupby(sq_item.item_code, sq_item.rate,sq.name)
    )
    
    if filters.get("request_for_quotation"):
        query = query.where(sq.custom_request_for_quotation == filters.get("request_for_quotation"))
    if filters.get("item_code"):
        query = query.where(sq_item.item_code == filters.get("item_code") )
        
    if filters.get("supplier"):
        query = query.where(sq.supplier.isin(filters.get("supplier")))
        
    if filters.get("supplier_quotation"):
        query = query.where(sq_item.parent.isin(filters.get("supplier_quotation")))
    
    if filters.get("project"):
        query = query.where(sq_item.project.isin(filters.get("project")))
        
    supplier_quotation_data = query.run(as_dict=True)
    return supplier_quotation_data

def get_columns(supplier_quotation_data):
    # Define static columns
    columns = [
        {"fieldname": "item_code", "label": _("Item Details"), "fieldtype": "Data", "width": 250},
        {"fieldname": "qty", "label": _("Qty"), "fieldtype": "Data", "width": 180}
    ]

    # Add dynamic columns for each supplier's rates and amounts
    unique_suppliers = list({data['supplier_name'] for data in supplier_quotation_data})

    for supplier in unique_suppliers:
        columns.extend([
            {"fieldname": f"{frappe.scrub(supplier)}_rate", "label": _(f"{supplier} Unit Rate"), "fieldtype": "Data", "width": 180},
            {"fieldname": f"{frappe.scrub(supplier)}_amount", "label": _(f"{supplier} Amount"), "fieldtype": "Data", "width": 180}
        ])

    return columns

def prepare_data(supplier_quotation_data):
    out = []
    item_details = []
    item_totals = defaultdict(float)

    # Group data by item code
    grouped_data = defaultdict(lambda: defaultdict(lambda: {"item_code":'',"rate": 0, "qty": 0, "amount": 0, "quotation_number": "", "name": ""}))

    for data in supplier_quotation_data:
        
        item_code = data.get("item_code")
        request_for_quotation_item = data.get('request_for_quotation_item')
        name = data.get("name")
        custom_remarks = data.get('custom_remarks')
        custom_delivery_terms = data.get('custom_delivery_terms')
        incoterm = data.get('incoterm')
        named_place = data.get('named_place')
        custom_payment_terms = data.get('custom_payment_terms')
        supplier_name = frappe.scrub(data.get("supplier_name"))
        rate = flt(data.get("rate"))
        qty = flt(data.get("qty"))
        amount = flt(data.get("amount"))
        quotation_number = data.get("parent")  # Assuming "parent" holds the quotation number
        
        # Store supplier data per item, including quotation number and name
        grouped_data[item_code][supplier_name] = {
            "rate": round(rate, 2),
            "qty": qty,
            "amount": amount,
            "quotation_number": quotation_number,
            "name": name,
            "custom_remarks":custom_remarks,
            "incoterm":incoterm, 
            "named_place":named_place,
            "custom_payment_terms" : custom_payment_terms,
            "custom_delivery_terms" : custom_delivery_terms 
        }
        
        item_totals[supplier_name] += amount
    
    quote_name_row = {"item_code": "<b>Quotation Name</b>"}
    for item_code, supplier_data in grouped_data.items():
        for supplier, data in supplier_data.items():
            quotation_name = data["name"]
            # Create clickable link to the quotation
            quote_name_row[f"{supplier}_rate"] = f"<a href='/app/supplier-quotation/{quotation_name}' target='_blank'>{quotation_name}</a>"

    out.append(quote_name_row)
    # Populate rows based on grouped data
    print(grouped_data)
    for item_code, supplier_data in grouped_data.items():
        
        # Row for item details and quantity
        row = {
            "item_code": item_code,
            "qty": next(iter(supplier_data.values())).get("qty", 0)
        }
       
        # Add quotation number first, followed by rate and amount for each supplier
        for supplier, data in supplier_data.items():
            item_details.append({
                "item_code":item_code,
                "supplier": supplier,
                "rate": data["rate"],
                "amount": data["amount"],
                "name":data["name"],
                "qty":next(iter(supplier_data.values())).get("qty", 0)
                })
            
            row[f"{supplier}_rate"] = data["rate"]
            row[f"{supplier}_amount"] = data["amount"]
           

        out.append(row)
        
    for data_name in supplier_quotation_data:
        for datas in item_details:
            if datas["item_code"] == data_name["item_code"] and datas["rate"] != data_name["rate"] and data_name.name == datas["name"]:
               

                # Initialize row_data with item_code and qty
                row_data = {
                    "item_code": data_name["item_code"],
                    "qty": data_name["qty"]
                }

                # Add supplier-specific rate and amount
                row_data[f"{datas['supplier']}_rate"] = data_name["rate"]
                row_data[f"{datas['supplier']}_amount"] = data_name["amount"]

                # Append the row data to out list
                out.append(row_data)

        
                


    # Add total row
    total_row = {"item_code": "<b>Total</b>"}
    for supplier, total_amount in item_totals.items():
        total_row[f"{supplier}_amount"] = frappe.format_value(total_amount, 'Currency')

    out.append(total_row)

    # Add quotation name row with clickable links for each supplier

    # Add rows for additional information (e.g., Remarks, Incoterms)
    remarks_row = {"item_code": "<b>Remarks</b>"}
    for item_code, supplier_data in grouped_data.items():
        for supplier, data in supplier_data.items():
            # Get the remarks for each supplier and item
            remarks_value = data.get('custom_remarks')
            supplier_scrubbed = f"{frappe.scrub(supplier)}_rate"  # Scrub the supplier name to create a valid key
            remarks_row[supplier_scrubbed] = f"{remarks_value or ''}</br>"

    out.append(remarks_row)
    incoterm_row = {"item_code": "<b>Incoterms</b>"}
    for item_code, supplier_data in grouped_data.items():
        for supplier, data in supplier_data.items():
        # Get the incoterm and named_place, concatenate them with a dash in between
            incoterm_value = data.get('incoterm', '')
            named_place_value = data.get('named_place', '')
            
            # Concatenate with a dash between the two values if both are present
            remarks_value = f"{incoterm_value} - {named_place_value}" if incoterm_value and named_place_value else incoterm_value or named_place_value
            
            # Scrub the supplier name to create a valid key
            supplier_scrubbed = f"{frappe.scrub(supplier)}_rate"  
            incoterm_row[supplier_scrubbed] = f"{remarks_value or ''}</br>"

    out.append(incoterm_row)
    payment_row = {"item_code": "<b>Payment Terms</b>"}
    for item_code, supplier_data in grouped_data.items():
        for supplier, data in supplier_data.items():
            # Get the remarks for each supplier and item
            remarks_value = data.get('custom_payment_terms')
            supplier_scrubbed = f"{frappe.scrub(supplier)}_rate"  # Scrub the supplier name to create a valid key
            payment_row[supplier_scrubbed] = f"{remarks_value or ''}</br>"

    out.append(payment_row)
    delivery_row = {"item_code": "<b>Delivery Terms</b>"}
    for item_code, supplier_data in grouped_data.items():
        for supplier, data in supplier_data.items():
            # Get the remarks for each supplier and item
            remarks_value = data.get('custom_delivery_terms')
            supplier_scrubbed = f"{frappe.scrub(supplier)}_rate"  # Scrub the supplier name to create a valid key
            delivery_row[supplier_scrubbed] = f"{remarks_value or ''}</br>"

    out.append(delivery_row)
    

    return out

@frappe.whitelist()
def item_query(doctype, txt, searchfield, start, page_len, filters):
    query = """
        SELECT item_code
        FROM `tabSupplier Quotation Item` 
        WHERE request_for_quotation = %(request_for_quotation)s
        AND docstatus < 2
        AND item_code LIKE %(txt)s
    """
    
    # If the project filter is provided, include it in the query
    if filters.get("project"):
        query += " AND project IN %(project)s"
        
    query += " ORDER BY item_code"

    return frappe.db.sql(query, {
        "request_for_quotation": filters.get("request_for_quotation"),
        "txt": "%%%s%%" % txt,
        "project": filters.get("project")
    })