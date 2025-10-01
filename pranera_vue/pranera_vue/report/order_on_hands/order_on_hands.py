# Copyright (c) 2025, Aravind and contributors
# For license information, please see license.txt


# from collections import defaultdict
# import frappe
# from frappe import _
# from frappe.query_builder.functions import Sum
# from frappe.utils import flt, today


# def execute(filters=None):
#     columns, data = [], []
#     data = get_data(filters)
#     columns = get_columns(filters)
#     return columns, data

# def get_columns(filters):
#     columns = [
#         {
#             "label": _("Date"),
#             "fieldname": "posting_date",
#             "fieldtype": "Date",
#             "width": 150,
#         },
#         {
#             "label": _("Delivery Date"),
#             "fieldname": "delivery_date",
#             "fieldtype": "Date",
#             "width": 150,
#         },
#         {
#             "label": _("Sales Order"),
#             "fieldname": "name",
#             "fieldtype": "Link",
#             "options": "Sales Order",
#             "width": 150,
#         },
#         {
#             "label": _("Item Code"),
#             "fieldname": "item_code",
#             "fieldtype": "Link",
#             "options": "Item",
#             "width": 200,
#         },
#         {
#             "label": _("Commercial Name"),
#             "fieldname": "commercial_name",
#             "fieldtype": "Data",
#             "width": 100,
#         },
#         {
#             "label": _("Color"),
#             "fieldname": "color",
#             "fieldtype": "Data",
#             "width": 200,
#         },
#         {
#             "label": _("Width"),
#             "fieldname": "width",
#             "fieldtype": "Data",
#             "width": 100,
#         },
#         {
#             "label": _("Qty"),
#             "fieldname": "qty",
#             "fieldtype": "Float",
#             "width": 90,
#         },
#         {
#             "label": _("Delivered Qty"),
#             "fieldname": "delivered_qty",
#             "fieldtype": "Float",
#             "width": 90,
#         },
#         {
#             "label": _("Pending Qty"),
#             "fieldname": "pending_qty",
#             "fieldtype": "Float",
#             "width": 90,
#         },
#         {
#             "label": _("Amount"),
#             "fieldname": "original_amount",
#             "fieldtype": "Float",
#             "width": 90,
#         },
#         {
#             "label": _("Item Status"),
#             "fieldname": "custom_item_status",
#             "fieldtype": "Data",
#             "width": 70,
#         },
#         {
#             "label": _("UOM"),
#             "fieldname": "stock_uom",
#             "fieldtype": "Data",
#             "width": 70,
#         },
#         {
#             "label": _("Customer"),
#             "fieldname": "customer",
#             "fieldtype": "Data",
#             "width": 100,
#         },
#         {
#             "label": _("Sales Person"),
#             "fieldname": "sales_person",
#             "fieldtype": "Data",
#             "width": 100,
#         },
#         {
#             "label": _("Parent Sales Person"),
#             "fieldname": "parent_sales_person",
#             "fieldtype": "Data",
#             "width": 100,
#         },
#         {
#             "label": _("Document status"),
#             "fieldname": "status",
#             "fieldtype": "Data",
#             "width": 70,
#         }
#     ]

#     return columns

# def get_data(filters):
#     data = []
#     sales_data = get_sales_order_data(filters)
#     data.extend(sales_data)
#     return data

# def get_sales_order_data(filters):
#     print("=== SQL DEBUG ===")
#     print("Filters in get_sales_order_data:", filters)
    
#     # Your existing query here...
#     query = """
#         SELECT
#             soi.item_code AS item_code,
#             soi.custom_commercial_name AS commercial_name,
#             soi.custom_color AS color,
#             soi.custom_width AS width,
#             soi.custom_item_status AS custom_item_status,
#             soi.qty AS qty,
#             soi.rate AS rate,
#             soi.amount AS original_amount,
#             COALESCE(soi.delivered_qty, 0) AS delivered_qty,
#             (soi.qty - COALESCE(soi.delivered_qty, 0)) AS pending_qty,
#             ROUND(
#                 CASE 
#                     WHEN soi.qty > 0 THEN 
#                         (COALESCE(soi.delivered_qty, 0) / soi.qty) * 100 
#                     ELSE 0 
#                 END, 2
#             ) AS delivered_qty_percent,
#             ROUND(
#                 CASE 
#                     WHEN soi.qty > 0 THEN 
#                         ((soi.qty - COALESCE(soi.delivered_qty, 0)) / soi.qty) * 100 
#                     ELSE 0 
#                 END, 2
#             ) AS pending_qty_percent,
#             (COALESCE(soi.delivered_qty, 0) * soi.rate) AS delivered_amount,
#             ((soi.qty - COALESCE(soi.delivered_qty, 0)) * soi.rate) AS pending_amount,
#             ROUND(
#                 CASE 
#                     WHEN soi.amount > 0 THEN 
#                         (COALESCE(soi.delivered_qty, 0) * soi.rate / soi.amount) * 100 
#                     ELSE 0 
#                 END, 2
#             ) AS amount_billed_percent,
#             soi.stock_uom AS stock_uom,
#             so.transaction_date AS posting_date,
#             so.customer AS customer,
#             st.sales_person,
#             sp.parent_sales_person,
#             so.name AS name,
#             so.naming_series AS series,
#             so.delivery_date AS delivery_date,
#             so.delivery_status AS delivery_status,
#             so.status AS status
#         FROM 
#             `tabSales Order Item` AS soi
#         LEFT JOIN 
#             `tabSales Order` AS so
#         ON 
#             so.name = soi.parent
#         LEFT JOIN `tabSales Team` st on st.parent = so.name
#         LEFT JOIN `tabSales Person` sp on st.sales_person = sp.name    
#         WHERE 
#             so.docstatus = 1
#     """

#     conditions = []
#     params = {}
    
#     print("Processing filters:", filters)
    
#     if filters.get("item_code"):
#         # Use LIKE for partial matching instead of exact match
#         conditions.append("soi.item_code LIKE %(item_code)s")
#         params["item_code"] = f"%{filters.get('item_code')}%"
#         print(f"Added item_code filter: {filters.get('item_code')} -> {params['item_code']}")
    
#     if filters.get("commercial_name"):
#         conditions.append("soi.custom_commercial_name LIKE %(commercial_name)s")
#         params["commercial_name"] = f"%{filters.get('commercial_name')}%"
    
#     if filters.get("color"):
#         conditions.append("soi.custom_color LIKE %(color)s")
#         params["color"] = f"%{filters.get('color')}%"

#     if filters.get("custom_item_status"):
#         custom_item_status = filters.get("custom_item_status")
#         if isinstance(custom_item_status, list):
#             conditions.append("soi.custom_item_status IN %(custom_item_status)s")
#             params["custom_item_status"] = custom_item_status
#         else:
#             conditions.append("soi.custom_item_status = %(custom_item_status)s")
#             params["custom_item_status"] = custom_item_status
    
#     if filters.get("from_date"):
#         conditions.append("so.transaction_date >= %(from_date)s")
#         params["from_date"] = filters.get("from_date")
#         print(f"Added from_date filter: {filters.get('from_date')}")  # Debug log

#     if filters.get("to_date"):
#         conditions.append("so.transaction_date <= %(to_date)s")
#         params["to_date"] = filters.get("to_date")
#         print(f"Added to_date filter: {filters.get('to_date')}")  # Debug log
    
#     if filters.get("delivery_status"):
#         conditions.append("so.delivery_status = %(delivery_status)s")
#         params["delivery_status"] = filters.get("delivery_status")
    
#     # Handle series filter (multiselect)
#     if filters.get("series"):
#         series = filters.get("series")
#         if isinstance(series, list):
#             conditions.append("so.naming_series IN %(series)s")
#             params["series"] = series
#         else:
#             conditions.append("so.naming_series = %(series)s")
#             params["series"] = series

#     # Sales Person filter with partial matching
#     if filters.get("sales_person"):
#         sales_person = filters.get("sales_person")
#         # Check if the sales person is a parent sales person
#         is_parent = frappe.db.get_value("Sales Person", sales_person, "is_group")
        
#         if is_parent:
#             # If it's a parent sales person, get all child sales persons
#             child_sales_persons = get_child_sales_persons(sales_person)
#             if child_sales_persons:
#                 conditions.append("(st.sales_person IN %(sales_persons)s OR sp.parent_sales_person = %(sales_person)s)")
#                 params["sales_persons"] = child_sales_persons
#                 params["sales_person"] = sales_person
#             else:
#                 conditions.append("sp.parent_sales_person = %(sales_person)s")
#                 params["sales_person"] = sales_person
#         else:
#             # If it's a regular sales person, show their data directly with partial matching
#             conditions.append("(st.sales_person LIKE %(sales_person)s OR sp.parent_sales_person LIKE %(sales_person)s)")
#             params["sales_person"] = f"%{sales_person}%"

#     if conditions:
#         query += " AND " + " AND ".join(conditions)

#     print("Final SQL query:", query)  # Debug log
#     print("Query parameters:", params)  # Debug log

#     return frappe.db.sql(query, params, as_dict=1)

# def get_child_sales_persons(parent_sales_person):
#     """Get all child sales persons for a given parent sales person"""
#     child_sales_persons = frappe.db.sql("""
#         SELECT name 
#         FROM `tabSales Person` 
#         WHERE parent_sales_person = %s 
#         OR name IN (
#             SELECT name FROM `tabSales Person` 
#             WHERE parent_sales_person IN (
#                 SELECT name FROM `tabSales Person` WHERE parent_sales_person = %s
#             )
#         )
#     """, (parent_sales_person, parent_sales_person), as_list=True)
    
#     # Flatten the list and include the parent itself
#     result = [parent_sales_person]
#     for child in child_sales_persons:
#         result.append(child[0])
    
#     return result


from collections import defaultdict
import frappe
from frappe import _
from frappe.query_builder.functions import Sum
from frappe.utils import flt, today


def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": _("Delivery Date"),
            "fieldname": "delivery_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": _("Sales Order"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 150,
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "label": _("Commercial Name"),
            "fieldname": "commercial_name",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Color"),
            "fieldname": "color",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Width"),
            "fieldname": "width",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 90,
        },
        {
            "label": _("Delivered Qty"),
            "fieldname": "delivered_qty",
            "fieldtype": "Float",
            "width": 90,
        },
        {
            "label": _("Pending Qty"),
            "fieldname": "pending_qty",
            "fieldtype": "Float",
            "width": 90,
        },
        {
            "label": _("Amount"),
            "fieldname": "original_amount",
            "fieldtype": "Float",
            "width": 90,
        },
        {
            "label": _("Item Status"),
            "fieldname": "custom_item_status",
            "fieldtype": "Data",
            "width": 70,
        },
        {
            "label": _("UOM"),
            "fieldname": "stock_uom",
            "fieldtype": "Data",
            "width": 70,
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Parent Sales Person"),
            "fieldname": "parent_sales_person",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Document status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 70,
        }
    ]

    return columns

def get_data(filters):
    data = []
    sales_data = get_sales_order_data(filters)
    data.extend(sales_data)
    return data

def get_sales_order_data(filters):
    print("=== SQL DEBUG START ===")
    print("Raw filters received:", filters)
    print("Filter types:", {k: type(v).__name__ for k, v in filters.items()})
    
    # Test query to check if any data exists with SKF
    test_query = """
        SELECT COUNT(*) as count, item_code 
        FROM `tabSales Order Item` 
        WHERE item_code LIKE '%%SKF%%'
        GROUP BY item_code
    """
    test_result = frappe.db.sql(test_query, as_dict=True)
    print("Test query result for SKF items:", test_result)
    
    # Your main query
    # query = """
    #     SELECT
    #         soi.item_code AS item_code,
    #         soi.custom_commercial_name AS commercial_name,
    #         soi.custom_color AS color,
    #         soi.custom_width AS width,
    #         soi.custom_item_status AS custom_item_status,
    #         soi.qty AS qty,
    #         soi.rate AS rate,
    #         soi.amount AS original_amount,
    #         COALESCE(soi.delivered_qty, 0) AS delivered_qty,
    #         (soi.qty - COALESCE(soi.delivered_qty, 0)) AS pending_qty,
    #         ROUND(
    #             CASE 
    #                 WHEN soi.qty > 0 THEN 
    #                     (COALESCE(soi.delivered_qty, 0) / soi.qty) * 100 
    #                 ELSE 0 
    #             END, 2
    #         ) AS delivered_qty_percent,
    #         ROUND(
    #             CASE 
    #                 WHEN soi.qty > 0 THEN 
    #                     ((soi.qty - COALESCE(soi.delivered_qty, 0)) / soi.qty) * 100 
    #                 ELSE 0 
    #             END, 2
    #         ) AS pending_qty_percent,
    #         (COALESCE(soi.delivered_qty, 0) * soi.rate) AS delivered_amount,
    #         ((soi.qty - COALESCE(soi.delivered_qty, 0)) * soi.rate) AS pending_amount,
    #         ROUND(
    #             CASE 
    #                 WHEN soi.amount > 0 THEN 
    #                     (COALESCE(soi.delivered_qty, 0) * soi.rate / soi.amount) * 100 
    #                 ELSE 0 
    #             END, 2
    #         ) AS amount_billed_percent,
    #         soi.stock_uom AS stock_uom,
    #         so.transaction_date AS posting_date,
    #         so.customer AS customer,
    #         st.sales_person,
    #         sp.parent_sales_person,
    #         so.name AS name,
    #         so.naming_series AS series,
    #         so.delivery_date AS delivery_date,
    #         so.delivery_status AS delivery_status,
    #         so.status AS status
    #     FROM 
    #         `tabSales Order Item` AS soi
    #     LEFT JOIN 
    #         `tabSales Order` AS so
    #     ON 
    #         so.name = soi.parent
    #     LEFT JOIN `tabSales Team` st on st.parent = so.name
    #     LEFT JOIN `tabSales Person` sp on st.sales_person = sp.name    
    #     WHERE 
    #         so.docstatus = 1
    # """

    query = """
        SELECT
            soi.item_code AS item_code,
            soi.commercial_name AS commercial_name,
            soi.color AS color,
            soi.width AS width,
            soi.custom_item_status AS custom_item_status,
            soi.qty AS qty,
            soi.rate AS rate,
            soi.amount AS original_amount,
            COALESCE(soi.delivered_qty, 0) AS delivered_qty,
            (soi.qty - COALESCE(soi.delivered_qty, 0)) AS pending_qty,
            ROUND(
                CASE 
                    WHEN soi.qty > 0 THEN 
                        (COALESCE(soi.delivered_qty, 0) / soi.qty) * 100 
                    ELSE 0 
                END, 2
            ) AS delivered_qty_percent,
            ROUND(
                CASE 
                    WHEN soi.qty > 0 THEN 
                        ((soi.qty - COALESCE(soi.delivered_qty, 0)) / soi.qty) * 100 
                    ELSE 0 
                END, 2
            ) AS pending_qty_percent,
            (COALESCE(soi.delivered_qty, 0) * soi.rate) AS delivered_amount,
            ((soi.qty - COALESCE(soi.delivered_qty, 0)) * soi.rate) AS pending_amount,
            ROUND(
                CASE 
                    WHEN soi.amount > 0 THEN 
                        (COALESCE(soi.delivered_qty, 0) * soi.rate / soi.amount) * 100 
                    ELSE 0 
                END, 2
            ) AS amount_billed_percent,
            soi.stock_uom AS stock_uom,
            so.transaction_date AS posting_date,
            so.customer AS customer,
            st.sales_person,
            sp.parent_sales_person,
            so.name AS name,
            so.naming_series AS series,
            so.delivery_date AS delivery_date,
            so.delivery_status AS delivery_status,
            so.status AS status
        FROM 
            `tabSales Order Item` AS soi
        LEFT JOIN 
            `tabSales Order` AS so
        ON 
            so.name = soi.parent
        LEFT JOIN `tabSales Team` st on st.parent = so.name
        LEFT JOIN `tabSales Person` sp on st.sales_person = sp.name    
        WHERE 
            so.docstatus = 1
    """

    conditions = []
    params = {}
    
    print("Building conditions...")
    
    # Item code filter with LIKE
    if filters.get("item_code"):
        item_code_filter = f"%{filters.get('item_code')}%"
        conditions.append("soi.item_code LIKE %(item_code)s")
        params["item_code"] = item_code_filter
        print(f"Added item_code filter: '{filters.get('item_code')}' -> '{item_code_filter}'")
    
    # Commercial name filter with LIKE
    if filters.get("commercial_name"):
        commercial_name_filter = f"%{filters.get('commercial_name')}%"
        conditions.append("soi.custom_commercial_name LIKE %(commercial_name)s")
        params["commercial_name"] = commercial_name_filter
        print(f"Added commercial_name filter: '{filters.get('commercial_name')}' -> '{commercial_name_filter}'")
    
    # Color filter with LIKE
    if filters.get("color"):
        color_filter = f"%{filters.get('color')}%"
        conditions.append("soi.custom_color LIKE %(color)s")
        params["color"] = color_filter
        print(f"Added color filter: '{filters.get('color')}' -> '{color_filter}'")

    # Item status filter
    if filters.get("custom_item_status"):
        custom_item_status = filters.get("custom_item_status")
        if isinstance(custom_item_status, list):
            conditions.append("soi.custom_item_status IN %(custom_item_status)s")
            params["custom_item_status"] = custom_item_status
        else:
            conditions.append("soi.custom_item_status = %(custom_item_status)s")
            params["custom_item_status"] = custom_item_status
        print(f"Added custom_item_status filter: {custom_item_status}")
    
    # Date filters
    if filters.get("from_date"):
        conditions.append("so.transaction_date >= %(from_date)s")
        params["from_date"] = filters.get("from_date")
        print(f"Added from_date filter: {filters.get('from_date')}")

    if filters.get("to_date"):
        conditions.append("so.transaction_date <= %(to_date)s")
        params["to_date"] = filters.get("to_date")
        print(f"Added to_date filter: {filters.get('to_date')}")
    
    # Delivery status filter
    if filters.get("delivery_status"):
        conditions.append("so.delivery_status = %(delivery_status)s")
        params["delivery_status"] = filters.get("delivery_status")
        print(f"Added delivery_status filter: {filters.get('delivery_status')}")
    
    # Handle series filter (multiselect)
    if filters.get("series"):
        series = filters.get("series")
        if isinstance(series, list):
            conditions.append("so.naming_series IN %(series)s")
            params["series"] = series
        else:
            conditions.append("so.naming_series = %(series)s")
            params["series"] = series
        print(f"Added series filter: {series}")

    # Sales Person filter with partial matching
    if filters.get("sales_person"):
        sales_person = filters.get("sales_person")
        print(f"Processing sales_person filter: {sales_person}")
        
        # Check if the sales person is a parent sales person
        is_parent = frappe.db.get_value("Sales Person", sales_person, "is_group")
        print(f"Sales person '{sales_person}' is_parent: {is_parent}")
        
        if is_parent:
            # If it's a parent sales person, get all child sales persons
            child_sales_persons = get_child_sales_persons(sales_person)
            print(f"Child sales persons: {child_sales_persons}")
            
            if child_sales_persons:
                conditions.append("(st.sales_person IN %(sales_persons)s OR sp.parent_sales_person = %(sales_person)s)")
                params["sales_persons"] = child_sales_persons
                params["sales_person"] = sales_person
            else:
                conditions.append("sp.parent_sales_person = %(sales_person)s")
                params["sales_person"] = sales_person
        else:
            # If it's a regular sales person, show their data directly with partial matching
            sales_person_filter = f"%{sales_person}%"
            conditions.append("(st.sales_person LIKE %(sales_person)s OR sp.parent_sales_person LIKE %(sales_person)s)")
            params["sales_person"] = sales_person_filter
            print(f"Added sales_person filter: '{sales_person}' -> '{sales_person_filter}'")

    # Build final query
    if conditions:
        query += " AND " + " AND ".join(conditions)

    print("Final SQL query:")
    print(query)
    print("Query parameters:", params)
    
    # Execute query
    try:
        result = frappe.db.sql(query, params, as_dict=1)
        print(f"Query executed successfully. Returned {len(result)} records")
        
        if result:
            print("First few records:")
            for i, record in enumerate(result[:3]):  # Show first 3 records
                print(f"Record {i+1}: {record.get('item_code')} - {record.get('posting_date')} - {record.get('name')}")
        else:
            print("No records returned. Let's test the query manually...")
            
            # Test the query without filters to see if we get any data
            base_query = """
                SELECT soi.item_code, so.transaction_date, so.name
                FROM `tabSales Order Item` AS soi
                LEFT JOIN `tabSales Order` AS so ON so.name = soi.parent
                WHERE so.docstatus = 1
                AND soi.item_code LIKE '%%SKF%%'
                LIMIT 5
            """
            base_result = frappe.db.sql(base_query, as_dict=True)
            print(f"Base test query result: {len(base_result)} records")
            for record in base_result:
                print(f"Test record: {record}")
                
    except Exception as e:
        print(f"SQL Error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        result = []
    
    print("=== SQL DEBUG END ===")
    return result

def get_child_sales_persons(parent_sales_person):
    """Get all child sales persons for a given parent sales person"""
    child_sales_persons = frappe.db.sql("""
        SELECT name 
        FROM `tabSales Person` 
        WHERE parent_sales_person = %s 
        OR name IN (
            SELECT name FROM `tabSales Person` 
            WHERE parent_sales_person IN (
                SELECT name FROM `tabSales Person` WHERE parent_sales_person = %s
            )
        )
    """, (parent_sales_person, parent_sales_person), as_list=True)
    
    # Flatten the list and include the parent itself
    result = [parent_sales_person]
    for child in child_sales_persons:
        result.append(child[0])
    
    return result