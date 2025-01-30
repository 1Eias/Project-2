import os
import json
import shutil
from fpdf import FPDF

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create required folders
folders = ["JSON_ORDER", "JSON_PROCESSED", "JSON_INVOICE", "JSON_ORDER_ERROR", "fonts"]
for folder in folders:
    os.makedirs(os.path.join(script_dir, folder), exist_ok=True)

# Folder paths
order_dir = os.path.join(script_dir, "JSON_ORDER")
processed_dir = os.path.join(script_dir, "JSON_PROCESSED")
invoice_dir = os.path.join(script_dir, "JSON_INVOICE")
error_dir = os.path.join(script_dir, "JSON_ORDER_ERROR")
fonts_dir = os.path.join(script_dir, "fonts")

def validate_order_data(order):
    """Validate required fields in the order data"""
    required_customer_fields = ['naam', 'adres', 'postcode', 'stad', 'KVK-nummer']
    customer = order.get("klant", {})
    
    for field in required_customer_fields:
        if field not in customer:
            raise KeyError(f"Missing required customer field: {field}")
            
    if not order.get("factuurnummer"):
        raise KeyError("Missing factuurnummer")

def generate_pdf(invoice_data, invoice_file_path):
    pdf = FPDF()
    pdf.add_page()

    # Font configuration
    font_path_regular = os.path.join(fonts_dir, "DejaVuSans.ttf")
    font_path_bold = os.path.join(fonts_dir, "DejaVuSans-Bold.ttf")
    font_path_italic = os.path.join(fonts_dir, "DejaVuSans-Oblique.ttf")

    if not all(os.path.exists(p) for p in [font_path_regular, font_path_bold, font_path_italic]):
        raise FileNotFoundError("Required font files are missing in fonts directory")

    # Register fonts
    pdf.add_font("DejaVu", style="", fname=font_path_regular)
    pdf.add_font("DejaVu", style="B", fname=font_path_bold)
    pdf.add_font("DejaVu", style="I", fname=font_path_italic)

    # Header Section
    pdf.set_font("DejaVu", size=16, style="B")
    pdf.cell(0, 10, text="Y.E TechWorld", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, text="Waar ideeën tot leven komen.", new_x="LMARGIN", new_y="NEXT", align="C")

    # Company Info
    pdf.cell(0, 10, text="Leerparkpromenade 100", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 10, text="3312 KW Dordrecht", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 10, text="Bedrijfsnummer: 06 12345678", new_x="LMARGIN", new_y="NEXT", align="C")

    # Customer Information
    pdf.set_font("DejaVu", size=12, style="B")
    pdf.cell(0, 10, text="Factuur voor:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", size=10)
    customer = invoice_data["customer"]
    pdf.cell(0, 10, text=f"Naam: {customer['naam']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Adres: {customer['adres']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Postcode: {customer['postcode']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Stad: {customer['stad']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"KVK-nummer: {customer['KVK-nummer']}", new_x="LMARGIN", new_y="NEXT")

    # Invoice Details
    pdf.set_font("DejaVu", size=12, style="B")
    pdf.cell(0, 10, text=f"Factuurnummer: {invoice_data['invoice_number']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Factuurdatum: {invoice_data['invoice_date']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Betaaltermijn: {invoice_data['payment_terms']}", new_x="LMARGIN", new_y="NEXT")

    # Products Table
    pdf.set_font("DejaVu", size=10, style="B")
    col_widths = [20, 80, 40, 40]
    headers = ["Aantal", "Omschrijving", "Prijs/stuk", "Totaal (excl. BTW)"]
    
    for width, header in zip(col_widths, headers):
        pdf.cell(width, 10, text=header, border=1)
    pdf.ln()

    pdf.set_font("DejaVu", size=10)
    for product in invoice_data["products"]:
        total = product["aantal"] * product["prijs_per_stuk_excl_btw"]
        pdf.cell(col_widths[0], 10, text=str(product["aantal"]), border=1)
        pdf.cell(col_widths[1], 10, text=product["productnaam"], border=1)
        pdf.cell(col_widths[2], 10, text=f"€{product['prijs_per_stuk_excl_btw']:.2f}", border=1)
        pdf.cell(col_widths[3], 10, text=f"€{total:.2f}", border=1)
        pdf.ln()

    # Totals
    totals = [
        ("Totaal Exclusief BTW", invoice_data['totals']['total_excl_vat']),
        ("BTW", invoice_data['totals']['total_vat']),
        ("Totaal Inclusief BTW", invoice_data['totals']['total_incl_vat'])
    ]
    
    pdf.set_font("DejaVu", size=10, style="B")
    for label, amount in totals:
        pdf.cell(sum(col_widths[:3]), 10, text=label, border=1)
        pdf.cell(col_widths[3], 10, text=f"€{amount:.2f}", border=1)
        pdf.ln()

    # Footer
    pdf.set_font("DejaVu", size=10)
    pdf.cell(0, 10, text="Maak alle betalingen over aan Y.E TechWorld", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 10, text="Bedankt voor uw zaken.", new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.output(invoice_file_path)
    print(f"✅ Created: {os.path.basename(invoice_file_path)}")

def process_order(order_file_path, invoice_dir):
    try:
        with open(order_file_path, "r") as f:
            data = json.load(f)

        order = data.get("factuur", {})
        validate_order_data(order)

        # Process products and totals
        products = order.get("producten", [])
        total_excl_vat = sum(p["aantal"] * p["prijs_per_stuk_excl_btw"] for p in products)
        total_vat = sum(p["aantal"] * p.get("btw_per_stuk", 0) for p in products)
        
        invoice_data = {
            "invoice_number": order["factuurnummer"],
            "invoice_date": order.get("factuurdatum", ""),
            "payment_terms": order.get("betaaltermijn", ""),
            "customer": order["klant"],
            "products": products,
            "totals": {
                "total_excl_vat": round(total_excl_vat, 2),
                "total_vat": round(total_vat, 2),
                "total_incl_vat": round(total_excl_vat + total_vat, 2)
            }
        }

        pdf_path = os.path.join(invoice_dir, f"invoice_{invoice_data['invoice_number']}.pdf")
        generate_pdf(invoice_data, pdf_path)
        shutil.move(order_file_path, os.path.join(processed_dir, os.path.basename(order_file_path)))

    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        print(f"❌ Error processing {os.path.basename(order_file_path)}: {str(e)}")
        shutil.move(order_file_path, os.path.join(error_dir, os.path.basename(order_file_path)))
    except Exception as e:
        print(f"❌ Unexpected error for {os.path.basename(order_file_path)}: {str(e)}")
        shutil.move(order_file_path, os.path.join(error_dir, os.path.basename(order_file_path)))

# Process all orders
for filename in os.listdir(order_dir):
    if filename.endswith(".json"):
        process_order(os.path.join(order_dir, filename), invoice_dir)

print("✨ Bulk processing complete!")