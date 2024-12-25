import frappe
from frappe.website.path_resolver import resolve_path as original_resolve_path
from urllib.parse import urlparse

def path_resolver(path: str):
    # Handle path with query parameters
    parsed_path = urlparse(path).path  # Only take the base path, ignoring the query string
    
    print(f"Resolving path: {parsed_path}")  # Log the path

    # Check if a short link exists for the path
    if frappe.db.exists("Short Link", {"short_link": parsed_path}):
        short_link = frappe.db.get_value(
            "Short Link",
            {"short_link": parsed_path},
            ["destination_url", "name"],
            as_dict=True,
        )

        click = frappe.new_doc("Short Link Click")
        request_headers = frappe.request.headers
        click.ip = request_headers.get("X-Real-Ip")
        click.user_agent = request_headers.get("User-Agent")
        click.referrer = request_headers.get('Referer')
        click.link = short_link.name
        click.insert().submit()
        frappe.db.commit() # to remove once MyISAM
        # Redirect to the destination URL of the short link
        frappe.redirect(short_link.destination_url)

    # Use the original path resolver if no short link was found
    return original_resolve_path(path)
