import frappe 
from frappe import _


# Todo: non_standard_fieldnames is to be decided
def get_data(**kwargs):
    return {
		"fieldname": "stock_entry",
		"non_standard_fieldnames": {
        "Sales Invoice": "custom_stock_entry",
			# "DocType Name": "Reference field name",
		},
		"internal_links": {
			"Purchase Order": ["items", "purchase_order"],
			"Subcontracting Order": ["items", "subcontracting_order"],
			"Subcontracting Receipt": ["items", "subcontracting_receipt"],
             "Sales Invoice": ["items", "custom_stock_entry"],
		},
		"transactions": [
			{
				"label": _("Reference"),
				"items": [
					"Purchase Order",
					"Subcontracting Order",
					"Subcontracting Receipt",
                   
				],
			},
   {"label": _("Sales Invoice"), "items": [ "Sales Invoice"]},
		],
	}