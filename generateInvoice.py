import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
from pdfkit.configuration import Configuration

def format_currency(value):
    return f"${value:,.2f}"

def amount_in_words(amount):
    # Dummy implementation for the sake of example
    return f"{amount} US Dollars only"

def generate_invoice(seller_details, billing_details, invoice_details, items):
    # Calculate derived parameters
    for item in items:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item['discount']
        item['tax_type'] = 'IGST'
        item['tax_rate'] = 10
        item['tax_amount_igst'] = item['net_amount'] * 0.10
        item['total_amount'] = item['net_amount'] + item['tax_amount_igst']
    
    total_amount = sum(item['total_amount'] for item in items)

    # Load the HTML template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('invoice_template.html')

    # Render the template with data
    html_out = template.render(
        seller_details=seller_details,
        billing_details=billing_details,
        invoice_details=invoice_details,
        items=items,
        total_amount=format_currency(total_amount),
        amount_in_words=amount_in_words(total_amount)
    )

    # Configure wkhtmltopdf path - adjust this path to where you've installed it
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Example path for Windows
    config = None
    if os.path.exists(wkhtmltopdf_path):
        config = Configuration(wkhtmltopdf=wkhtmltopdf_path)

    # Generate PDF
    pdfkit.from_string(html_out, 'invoice.pdf', options={
        'enable-local-file-access': None
    }, configuration=config)

# Sample data
seller_details = {
    "name": " Strauss Consulting",
    "address": "Max-Joseph-Platz 2",
    "city": "München",
    "pincode": "80539",
    "country": "Germany"
}

billing_details = {
    "name": "Cronus International Ltd.",
    "address": "7122 South Ashford Street",
    "city": "Atlanta",
    "state": "Georgia",
    "pincode": "31772",
    "country": "United States"
}

invoice_details = {
    "invoice_no": "INV-001",
    "invoice_date": "2025-07-01"
}

items = [
    {"description": "Business Strategy Consultation - Hourly", "unit_price": 120, "quantity": 10, "discount": 0, "tax_rate": 10},
    {"description": "Leadership Training and Coaching", "unit_price": 350, "quantity": 4, "discount": 0, "tax_rate": 10}
]
generate_invoice(seller_details, billing_details, invoice_details, items)
