# Invoice Generator

This project automates the creation of PDF invoices from YAML data files using Python, Jinja2 templating, and pdfkit.

## Features

- **Professional Invoices:** Generates professional-looking PDF invoices.
- **Tax Calculation:** Supports tax calculations with configurable tax rates per item.
- **Dynamic Totals:** Automatically calculates totals, tax amounts, and net amounts for each item.
- **Detailed Information:** Includes comprehensive seller, billing, and invoice details.
- **Customizable:** Easily customizable with your company logo.
- **Batch Processing:** Process multiple invoice files at once from the inputs directory.
- **Organized Output:** Maintains the same folder structure in outputs as in the inputs directory.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- pdfkit
- Jinja2
- PyYAML
- wkhtmltopdf (required by pdfkit for PDF rendering)

### Installing Dependencies

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/invoice-generator.git
   cd invoice-generator
   ```

2. Install Python dependencies:
   ```bash
   pip install pdfkit jinja2 pyyaml
   ```

3. Install wkhtmltopdf:
   - **Ubuntu/Debian:**
     ```bash
     sudo apt-get install wkhtmltopdf
     ```
   - **macOS:**
     ```bash
     brew install wkhtmltopdf
     ```
   - **Windows:** Download and install from [wkhtmltopdf website](https://wkhtmltopdf.org/downloads.html).

## Usage

1. **Prepare Your Data:**
   - Create YAML files with your invoice data in the `inputs` directory
   - You can organize your files into subdirectories (e.g., by test type or client)
   - See the example structure in the `inputs` directory

2. **YAML File Structure:**
   ```yaml
   seller_details:
     name: "Company Name"
     address: "Street Address"
     city: "City"
     pincode: "Postal Code"
     country: "Country"

   billing_details:
     name: "Client Name"
     address: "Client Address"
     city: "Client City"
     state: "Client State"
     pincode: "Client Postal Code"
     country: "Client Country"

   invoice_details:
     invoice_no: "INV-001"
     invoice_date: "YYYY-MM-DD"

   items:
     - description: "Item Description"
       unit_price: 100
       quantity: 5
       discount: 20
       tax_rate: 10
   ```

3. **Customize Invoice Layout (Optional):**
   - Modify the HTML structure in `invoice_template.html` to adjust the invoice layout.

4. **Generate Invoices:**
   ```bash
   python generateInvoice.py
   ```

5. **View Invoices:**
   - The generated PDF invoices will be saved in the `outputs` directory, maintaining the same folder structure as the `inputs` directory.

## Project Structure

```
├── generateInvoice.py      # Main script for invoice generation
├── invoice_template.html   # HTML template for invoice layout
├── logo.png               # Your company logo
├── inputs/                # Input YAML files
│   └── [categories]/      # Organize by categories (optional)
│       └── [data].yaml    # Invoice data
└── outputs/              # Generated PDF invoices
    └── [categories]/     # Matching the inputs structure
        └── [data].pdf    # Generated invoice PDFs
```

## Customization

- **Invoice Template:** Adjust `invoice_template.html` to change the layout, styling, or content of the invoice.
- **Data Formatting:** Modify `format_currency` and `amount_in_words` functions in `generateInvoice.py` as per your requirements.
- **Images:** Replace `logo.png` with your actual company logo.

## Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request with your improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
