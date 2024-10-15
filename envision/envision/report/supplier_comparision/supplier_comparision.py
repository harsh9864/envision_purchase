# # Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt
from collections import defaultdict
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        return [], []

    supplier_quotation_data = get_data(filters)

    # Dynamically generate columns based on suppliers
    columns = get_columns(supplier_quotation_data)

    data = prepare_data(supplier_quotation_data)
    message = get_message()
    cmt = get_comment_data(filters)
    # print(cmt)
    return columns, data, message

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
            sq.workflow_state,
            sq.supplier.as_("supplier_name"),
            sq.custom_request_for_quotation,
            sq.name,
            sq.custom_remarks,
        )
        .where(
            (sq_item.parent == sq.name)
            & (sq_item.docstatus < 2)
            & (sq.company == filters.get("company"))
            & (sq.transaction_date.between(filters.get("from_date"), filters.get("to_date")))
        )
    )
    if filters.get("request_for_quotation"):
        query = query.where(sq.custom_request_for_quotation == filters.get("request_for_quotation") )
    
    if filters.get("item_code"):
        query = query.where(sq_item.item_code == filters.get("item_code") )
        
    if filters.get("supplier"):
        query = query.where(sq.supplier.isin(filters.get("supplier")))
        
    if filters.get("supplier_quotation"):
        query = query.where(sq_item.parent.isin(filters.get("supplier_quotation")))
        
    if filters.get("request_for_quotation"):
        query = query.where(sq_item.request_for_quotation == filters.get("request_for_quotation"))

	
    supplier_quotation_data = query.run(as_dict=True)

    return supplier_quotation_data

def get_comment_data(filters=None):
    cmt = frappe.qb.DocType("Comment")
    

    query = (
        frappe.qb.from_(cmt)
        .select(
            cmt.name,
            cmt.comment_type,
            cmt.comment_email,
            cmt.reference_name,
            cmt.reference_doctype,
            cmt.content,
            cmt.creation
        )
        .where(
            (cmt.reference_doctype == "Supplier Quotation")
            &(cmt.comment_type == "Workflow")
        )
    )
   

	
    cmt_data = query.run(as_dict=True)
    
    return cmt_data

def get_columns(supplier_quotation_data):
    # Define the first static column (for Item Code/Rate/Qty/Amount rows)
    columns = [{"fieldname": "item_code", "label": _("Items Details"), "fieldtype": "Data", "width": 350}]

    # Get unique suppliers from the fetched data
    unique_suppliers = list({data['supplier_name'] for data in supplier_quotation_data})

    # Dynamically create columns for each supplier
    for supplier in unique_suppliers:
        columns.append({
            "fieldname": frappe.scrub(supplier),  # Convert supplier name to a valid fieldname
            "label": _(supplier),
            "fieldtype": " ",
            "width": 250
        })

    return columns
def prepare_data(supplier_quotation_data):
    out = []
    item_totals = defaultdict(float)  # Store total amounts per supplier

    # Group data by item code
    grouped_data = defaultdict(lambda: defaultdict(lambda: {
        "rate": 0, "qty": 0, "amount": 0, "workflow_state": "", "remarks": "", "name": ""}))

    for data in supplier_quotation_data:
        item_code = data.get("item_code")
        supplier_name = frappe.scrub(data.get("supplier_name"))
        name = data.get("name")
        rate = flt(data.get("rate"))
        qty = flt(data.get("qty"))
        amount = flt(data.get("amount"))
        workflow_state = data.get("workflow_state", "")  # Get workflow_state
        remarks = data.get("custom_remarks", "")  # Get remarks (custom_remarks)

        # Store rate, qty, amount, workflow state, and remarks for each supplier under each item
        grouped_data[item_code][supplier_name]["rate"] = round(rate, 2)  # Rounded to 2 decimal places
        grouped_data[item_code][supplier_name]["qty"] = qty
        grouped_data[item_code][supplier_name]["amount"] = amount
        grouped_data[item_code][supplier_name]["name"] = name   
        grouped_data[item_code][supplier_name]["workflow_state"] = workflow_state  # Store workflow state
        grouped_data[item_code][supplier_name]["remarks"] = remarks  # Store remarks

        # Keep track of total amounts per supplier
        item_totals[supplier_name] += amount

    # Prepare rows for each item code, inserting rows for Rate, Quantity, and Amount
    for item_code, supplier_data in grouped_data.items():
        # First row will show Item Code
        row_item_code = {"item_code": f"<b> {item_code}</b>"}
        row_rate = {"item_code": f"Rate : "}
        row_qty = {"item_code": "  Quantity : "}
        row_amount = {"item_code": "  Amount :"}

        for supplier, data in supplier_data.items():
            supplier_scrubbed = frappe.scrub(supplier)
            quotation_link = f"<a href='/app/supplier-quotation/{data['name']}' target='_blank'>{data['name']}</a>"
            row_item_code[supplier_scrubbed] = f"<b>{quotation_link}</b>" 
            row_rate[supplier_scrubbed] = f"{data['rate']:.2f}"  # Format rate with 2 decimal places
            row_qty[supplier_scrubbed] = f"{data['qty']:.2f}" 
            row_amount[supplier_scrubbed] = f"{data['amount']:.2f}" 

        out.append(row_item_code)  # Insert Item Code row
        out.append(row_rate)       # Insert Rate row
        out.append(row_qty)        # Insert Quantity row
        out.append(row_amount)     # Insert Amount row

    # Add total row at the end with bolded currency fields
    total_row = {"item_code": "<b>Total Amount</b>"}
    for supplier, total_amount in item_totals.items():
        supplier_scrubbed = frappe.scrub(supplier)
        
        # Check if workflow_state is "Pending at HOD" or "Pending at Director"
        workflow_state = grouped_data.get(list(grouped_data.keys())[0], {}).get(supplier, {}).get("workflow_state", "")
        
        if workflow_state in ["Pending At HOD", "Pending At Director"]:
            # If workflow state is pending, bold the total amount
            total_row[supplier_scrubbed] = f"<div style='font-weight:bold;color:green'>{frappe.format_value(total_amount, 'Currency')}</div>"
        else:
            # Normal display without bold
            total_row[supplier_scrubbed] = frappe.format_value(total_amount, 'Currency')

    out.append(total_row)

    # Add remarks row at the end
    remarks_row = {"item_code": "<b>Remarks</b>"}
    for supplier in item_totals.keys():
        supplier_scrubbed = frappe.scrub(supplier)
        
        # Get the remarks for each supplier
        remarks_value = grouped_data.get(list(grouped_data.keys())[0], {}).get(supplier, {}).get("remarks", "")
        remarks_row[supplier_scrubbed] = f"{remarks_value or ''}</br>"

    out.append(remarks_row)

    # Add HOD approval date and sign
    comments = get_comment_data()

    hod_date = {"item_code": "<b>HOD Approval Date</b>"}
    hod_sign = {"item_code": "<b>HOD Approval Sign</b>"}
    
    for supplier in item_totals.keys():
        supplier_scrubbed = frappe.scrub(supplier)
        quotation_name = grouped_data.get(list(grouped_data.keys())[0], {}).get(supplier, {}).get("name", "")
        
        # Search for the comment data for each supplier quotation
        for cmt in comments:
            if cmt.reference_name == quotation_name and cmt.content == "HOD approval":
                hod_date[supplier_scrubbed] = frappe.format_value(cmt.creation, 'Date')   # HOD approval date (creation)
                hod_sign[supplier_scrubbed] = f"{cmt.comment_email or ''}</br>"  # HOD approval sign (comment email)
    
    out.append(hod_date)
    out.append(hod_sign)

    # Director approval date and sign (you can apply similar logic here)
    director_date = {"item_code": "<b>Director Approval Date</b>"}
    director_sign = {"item_code": "<b>Director Approval Sign</b>"}

    for supplier in item_totals.keys():
        supplier_scrubbed = frappe.scrub(supplier)
        # Similar logic to fill director details if available
        quotation_name = grouped_data.get(list(grouped_data.keys())[0], {}).get(supplier, {}).get("name", "")
        
        # Search for the comment data for each supplier quotation
        for cmt in comments:
            if cmt.reference_name == quotation_name and cmt.content == "Director Approval":
                director_date[supplier_scrubbed] = frappe.format_value(cmt.creation, 'Date')   # HOD approval date (creation)
                director_sign[supplier_scrubbed] = f"{cmt.comment_email or ''}</br>"  # HOD approval sign (comment email)
        
    out.append(director_date)
    out.append(director_sign)

    return out


def get_message():
    return """<span class="indicator">
        Valid till : &nbsp;&nbsp;
        </span>
        <span class="indicator orange">
        Expires in a week or less
        </span>
        &nbsp;&nbsp;
        <span class="indicator red">
        Expires today / Already Expired
        </span>"""


