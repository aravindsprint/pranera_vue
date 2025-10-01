# pranera_vue/pranera_vue/api/sales_order_api.py

# import frappe
# from frappe import _
# import json

# @frappe.whitelist()
# def get_sales_order_report(filters=None):
#     """
#     API endpoint to get sales order report data
#     Accepts filters as JSON string
#     """
#     try:
#         # Parse filters if provided
#         filter_dict = {}
#         if filters:
#             if isinstance(filters, str):
#                 filter_dict = json.loads(filters)
#             else:
#                 filter_dict = filters
        
#         # Get data using your existing function
#         from pranera_vue.pranera_vue.report.order_on_hands.order_on_hands import get_sales_order_data
#         data = get_sales_order_data(filter_dict)
        
#         return {
#             "message": {
#                 "message": data
#             }
#         }
    
#     except Exception as e:
#         frappe.log_error(f"Error in sales order report API: {str(e)}")
#         return {
#             "error": str(e)
#         }

# pranera_vue/pranera_vue/api/sales_order_api.py

import frappe
from frappe import _
import json

# @frappe.whitelist()
# def get_sales_order_report(filters=None):
#     """
#     API endpoint to get sales order report data
#     Accepts filters as JSON string
#     """
#     try:
#         # Parse filters if provided
#         filter_dict = {}
#         if filters:
#             if isinstance(filters, str):
#                 filter_dict = json.loads(filters)
#             else:
#                 filter_dict = filters
        
#         # Get data using your existing function
#         from pranera_vue.pranera_vue.report.order_on_hands.order_on_hands import get_sales_order_data
        
#         data = get_sales_order_data(filter_dict)
        
#         return {
#             "success": True,
#             "data": data,
#             "count": len(data)
#         }
    
#     except Exception as e:
#         frappe.log_error(f"Error in sales order report API: {str(e)}")
#         return {
#             "success": False,
#             "error": str(e),
#             "data": []
#         }

import frappe
from frappe import _
import json

@frappe.whitelist()
def get_sales_order_report(filters=None):
    """
    API endpoint to get sales order report data
    Accepts filters as JSON string or GET parameters
    """
    try:
        # Parse filters if provided
        filter_dict = {}
        if filters:
            if isinstance(filters, str):
                filter_dict = json.loads(filters)
            else:
                filter_dict = filters
        else:
            # If no filters parameter, check GET parameters from frappe.local.form_dict
            filter_dict = dict(frappe.local.form_dict)
            # Remove system parameters
            for key in ['cmd', 'csrf_token', '_']:
                filter_dict.pop(key, None)
        
        print("=== API DEBUG START ===")
        print("Raw filters received:", filter_dict)
        print("Filter types:", {k: type(v).__name__ for k, v in filter_dict.items()})
        
        # Clean and validate date formats
        if 'from_date' in filter_dict and filter_dict['from_date']:
            # Ensure date format is correct
            try:
                from datetime import datetime
                # Validate date format
                datetime.strptime(filter_dict['from_date'], '%Y-%m-%d')
                print(f"Valid from_date: {filter_dict['from_date']}")
            except ValueError as e:
                print(f"Invalid from_date format: {filter_dict['from_date']}, error: {e}")
                
        if 'to_date' in filter_dict and filter_dict['to_date']:
            try:
                from datetime import datetime
                datetime.strptime(filter_dict['to_date'], '%Y-%m-%d')
                print(f"Valid to_date: {filter_dict['to_date']}")
            except ValueError as e:
                print(f"Invalid to_date format: {filter_dict['to_date']}, error: {e}")
        
        # Get data using your existing function
        from pranera_vue.pranera_vue.report.order_on_hands.order_on_hands import get_sales_order_data
        
        data = get_sales_order_data(filter_dict)
        
        response = {
            "success": True,
            "data": data,
            "count": len(data) if data else 0
        }
        
        print("API Response:", response)
        print("=== API DEBUG END ===")
        
        return response
    
    except Exception as e:
        print("=== API ERROR ===")
        print("Error:", str(e))
        import traceback
        print("Traceback:", traceback.format_exc())
        print("=== END API ERROR ===")
        
        frappe.log_error(f"Error in sales order report API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": []
        }

@frappe.whitelist()
def get_sales_order_report_with_columns(filters=None):
    """
    API endpoint to get sales order report data with columns
    Accepts filters as JSON string
    """
    try:
        # Parse filters if provided
        filter_dict = {}
        if filters:
            if isinstance(filters, str):
                filter_dict = json.loads(filters)
            else:
                filter_dict = filters
        
        # Import the required functions
        from pranera_vue.pranera_vue.report.order_on_hands.order_on_hands import get_sales_order_data, get_columns
        
        data = get_sales_order_data(filter_dict)
        columns = get_columns(filter_dict)
        
        return {
            "success": True,
            "data": data,
            "columns": columns,
            "count": len(data)
        }
    
    except Exception as e:
        frappe.log_error(f"Error in sales order report API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "columns": []
        }

@frappe.whitelist()
def get_sales_persons():
    """
    API endpoint to get list of sales persons for filter dropdown
    """
    try:
        sales_persons = frappe.db.sql("""
            SELECT name, sales_person_name, is_group, parent_sales_person 
            FROM `tabSales Person` 
            ORDER BY is_group DESC, sales_person_name
        """, as_dict=True)
        
        return {
            "success": True,
            "data": sales_persons
        }
    
    except Exception as e:
        frappe.log_error(f"Error in get_sales_persons API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": []
        }

@frappe.whitelist()
def get_filter_options():
    """
    API endpoint to get filter options for the report
    """
    try:
        # Get commercial names
        commercial_names = frappe.db.sql("""
            SELECT DISTINCT custom_commercial_name 
            FROM `tabSales Order Item` 
            WHERE custom_commercial_name IS NOT NULL AND custom_commercial_name != ''
            ORDER BY custom_commercial_name
        """, as_list=True)
        
        # Get colors
        colors = frappe.db.sql("""
            SELECT DISTINCT custom_color 
            FROM `tabSales Order Item` 
            WHERE custom_color IS NOT NULL AND custom_color != ''
            ORDER BY custom_color
        """, as_list=True)
        
        # Get item status options
        item_statuses = frappe.db.sql("""
            SELECT DISTINCT custom_item_status 
            FROM `tabSales Order Item` 
            WHERE custom_item_status IS NOT NULL AND custom_item_status != ''
            ORDER BY custom_item_status
        """, as_list=True)
        
        # Get naming series
        series = frappe.db.sql("""
            SELECT DISTINCT naming_series 
            FROM `tabSales Order` 
            WHERE naming_series IS NOT NULL AND naming_series != ''
            ORDER BY naming_series
        """, as_list=True)
        
        return {
            "success": True,
            "data": {
                "commercial_names": [item[0] for item in commercial_names],
                "colors": [item[0] for item in colors],
                "item_statuses": [item[0] for item in item_statuses],
                "series": [item[0] for item in series]
            }
        }
    
    except Exception as e:
        frappe.log_error(f"Error in get_filter_options API: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": {}
        }

        
# from pranera_vue.pranera_vue.report.order_on_hands.order_on_hands import get_sales_order_data
# filters = {"sales_person": "Sivabalan"}
# data = get_sales_order_data(filters)
# len(data)

# http://localhost:8000/api/method/pranera_vue.pranera_vue.api.sales_order_api.get_sales_order_report

# /api/method/pranera_vue.api.get_sales_order_report