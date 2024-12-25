import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path

def path_resolver(path: str):
    frappe.logger().info(f"Resolving path: {path}")  # Log the path
    if frappe.db.exists("Short Link", {"short_link": path}):
        destination = frappe.db.get_value("Short Link", {"short_link": path}, "destination_url")
        frappe.logger().info(f"Redirecting to: {destination}")  # Log the destination URL
        frappe.redirect(destination)
    return original_resolve_path(path)
