app_name = "envision"
app_title = "Envision"
app_publisher = "Rutika"
app_description = "Envision Enviro"
app_email = "rutika@sanskartechnolab.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "envision",
# 		"logo": "/assets/envision/logo.png",
# 		"title": "Envision",
# 		"route": "/envision",
# 		"has_permission": "envision.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/envision/css/envision.css"
# app_include_js = "/assets/envision/js/envision.js"

# include js, css files in header of web template
# web_include_css = "/assets/envision/css/envision.css"
# web_include_js = "/assets/envision/js/envision.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "envision/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "envision/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "envision.utils.jinja_methods",
# 	"filters": "envision.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "envision.install.before_install"
# after_install = "envision.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "envision.uninstall.before_uninstall"
# after_uninstall = "envision.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "envision.utils.before_app_install"
# after_app_install = "envision.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "envision.utils.before_app_uninstall"
# after_app_uninstall = "envision.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "envision.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"envision.tasks.all"
# 	],
# 	"daily": [
# 		"envision.tasks.daily"
# 	],
# 	"hourly": [
# 		"envision.tasks.hourly"
# 	],
# 	"weekly": [
# 		"envision.tasks.weekly"
# 	],
# 	"monthly": [
# 		"envision.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "envision.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "envision.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "envision.task.get_dashboard_data"
# }
override_doctype_dashboards = {
    "Stock Entry": "envision.public.override.get_data",
 
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["envision.utils.before_request"]
# after_request = ["envision.utils.after_request"]

# Job Events
# ----------
# before_job = ["envision.utils.before_job"]
# after_job = ["envision.utils.after_job"]

# User Data Protection
# --------------------
doctype_js = {
    "Purchase Invoice" : "public/js/purchase_invoice.js",
    "Supplier Quotation" : "public/js/supplier_quotation.js",
    "Request for Quotation" : "public/js/request_for_quotation.js",
    "Material Request" : "public/js/material_request.js",
    "Purchase Receipt" : "public/js/purchase_receipt.js",
    "Purchase Order" : "public/js/purchase_order.js",
    "Sales Order" : "public/js/sales _order.js",
    "Stock Entry" : "public/js/stock_entry.js"
}
doctype_list_js = {"Supplier Quotation" : "public/js/supplier quotation List view button multiple.js"
}
# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"envision.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


fixtures = [
     "Workflow",
     "Workflow State",
     "Workflow Action Master",
    #  {
    #     "dt": "Custom DocPerm",
    #     "filters": [
    #         [
    #             "parent",
    #             "in",
    #             [
    #                 "Material Request",
    #                 "Request For Quotation",
    #                 "Supplier Quotation",
    #                 "Purchase Order",
    #                 "Purchase Invoice",
    #                 "Stock Entry"
    #             ],
    #         ]
    #     ],
    # },
    {"dt":"Print Format","filters":[
        [
        "module","in",[
                "Envision"
            ]
        ]
    ]},
    {"dt":"Custom Field","filters":[
        [
        "module","in",[
                "Envision"
            ]
        ]
    ]},
    {"dt":"Property Setter","filters":[
        [
        "module","in",[
                "Envision"
            ]
        ]
    ]}
]