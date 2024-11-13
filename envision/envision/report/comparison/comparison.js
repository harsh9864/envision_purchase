// Copyright (c) 2024, Rutika and contributors
// For license information, please see license.txt

// frappe.query_reports["Supplier Comparision"] = {
// 	"filters": [

// 	]
// };
// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Comparison"] = {
	filters: [
		{
			fieldtype: "Link",
			label: __("Company"),
			options: "Company",
			fieldname: "company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80",
			reqd: 1,
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Project", txt);
			},
		},
		{
			default: "",
			options: "Item",
			label: __("Item"),
			fieldname: "item_code",
			fieldtype: "Link",
			get_query: () => {
				let quote = frappe.query_report.get_filter_value("request_for_quotation");
				let project = frappe.query_report.get_filter_value("project");
				let company = frappe.query_report.get_filter_value("company");
				
                    return {
                        query: "envision.envision.report.comparison.comparison.item_query",
                        filters: {
                            request_for_quotation: quote,
                            project: project, // Pass project filter
							company: company
                        },
                    };
                
			
			},
		},
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "MultiSelectList",
			
			get_data: function (txt) {
				return frappe.db.get_link_options("Supplier", txt);
			},
		},	
		{
			fieldtype: "MultiSelectList",
			label: __("Supplier Quotation"),
			fieldname: "supplier_quotation",
			default: "",
			get_data: function (txt) {
				return frappe.db.get_link_options("Supplier Quotation", txt, { docstatus: ["<", 2] });
			},
		},
		{
			fieldtype: "Link",
			label: __("Request for Quotation"),
			options: "Request for Quotation",
			fieldname: "request_for_quotation",
			default: "",
			get_query: () => {
				return { filters: { docstatus: ["<", 2] } };
			},
		},
		
		
	],
	 
	formatter: (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "supplier" && data.supplier) {
			if (frappe.datetime.get_diff(data.supplier, frappe.datetime.nowdate()) <= 1) {
				value = `<div style="color:red">${value}</div>`;
			} else if (frappe.datetime.get_diff(data.valid_till, frappe.datetime.nowdate()) <= 7) {
				value = `<div style="color:darkorange">${value}</div>`;
			}
		}
		
		if (column.fieldname === "price_per_unit" && data.price_per_unit && data.min && data.min === 1) {
			value = `<div style="color:green">${value}</div>`;
		}
		return value;
	},

};
