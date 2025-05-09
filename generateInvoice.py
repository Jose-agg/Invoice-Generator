import pdfkit
from jinja2 import Environment, FileSystemLoader
import os
import yaml
from pdfkit.configuration import Configuration

def format_currency(value):
    return f"${value:,.2f}"

def amount_in_words(amount):
    # Dummy implementation for the sake of example
    return f"{amount} US Dollars only"

def generate_invoice(seller_details, billing_details, invoice_details, items, output_path=None):
    # Calculate derived parameters
    for item in items:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item['discount']
        item['tax_amount'] = item['net_amount'] / item['tax_rate']
        item['total_amount'] = item['net_amount'] + item['tax_amount']
    
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

    # Configure wkhtmltopdf path
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = None
    if os.path.exists(wkhtmltopdf_path):
        config = Configuration(wkhtmltopdf=wkhtmltopdf_path)

    # Generate PDF
    if output_path is None:
        output_path = 'invoice.pdf'
    
    pdfkit.from_string(html_out, output_path, options={
        'enable-local-file-access': None
    }, configuration=config)
    
    print(f"Invoice PDF generated: {output_path}")

def process_invoice_file(yaml_file_path):
    # Extract the file name without extension and parent directory
    file_name = os.path.basename(yaml_file_path)
    invoice_name = os.path.splitext(file_name)[0]
    
    # Get the category folder (parent directory of the yaml file)
    relative_path = os.path.relpath(yaml_file_path, 'inputs')
    category_dir = os.path.dirname(relative_path)
    
    # Read YAML file
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    # Define output PDF path maintaining the same folder structure
    if category_dir:
        output_dir = os.path.join('outputs', category_dir)
        # Create the category directory in outputs if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_pdf_path = os.path.join(output_dir, f"{invoice_name}.pdf")
    else:
        output_pdf_path = os.path.join('outputs', f"{invoice_name}.pdf")
    
    # Generate invoice
    generate_invoice(
        data['seller_details'], 
        data['billing_details'], 
        data['invoice_details'], 
        data['items'],
        output_pdf_path
    )
    
    return output_pdf_path

def process_all_invoices():
    # Check if inputs directory exists
    if not os.path.exists('inputs'):
        print("Error: 'inputs' directory not found")
        return
    
    # Create outputs directory if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    # Process all YAML files in inputs directory and its subdirectories
    processed_count = 0
    for root, dirs, files in os.walk('inputs'):
        yaml_files = [f for f in files if f.endswith(('.yaml', '.yml'))]
        
        for yaml_file in yaml_files:
            yaml_file_path = os.path.join(root, yaml_file)
            try:
                output_path = process_invoice_file(yaml_file_path)
                print(f"Processed {yaml_file_path} -> {output_path}")
                processed_count += 1
            except Exception as e:
                print(f"Error processing {yaml_file_path}: {str(e)}")
    
    if processed_count == 0:
        print("No YAML files found in the inputs directory or its subdirectories")
    else:
        print(f"Successfully processed {processed_count} invoice files")

# Main execution point
if __name__ == "__main__":
    process_all_invoices()
