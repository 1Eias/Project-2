import os
import json
import shutil
from fpdf import FPDF

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create required folders (added JSON_ORDER_ERROR)
folders = ["JSON_ORDER", "JSON_PROCESSED", "JSON_INVOICE", "Fonts", "JSON_ORDER_ERROR"]
for folder in folders:
    os.makedirs(os.path.join(script_dir, folder), exist_ok=True)

# Folder paths (added error_dir)
order_dir = os.path.join(script_dir, "JSON_ORDER")
processed_dir = os.path.join(script_dir, "JSON_PROCESSED")
invoice_dir = os.path.join(script_dir, "JSON_INVOICE")
fonts_dir = os.path.join(script_dir, "Fonts")
error_dir = os.path.join(script_dir, "JSON_ORDER_ERROR")  # New error directory

def generate_pdf(invoice_data, invoice_file_path):
    try:
        pdf = FPDF()
        pdf.add_page()

        # Add Unicode font
        font_path_regular = os.path.join(fonts_dir, "DejaVuSans.ttf")
        font_path_bold = os.path.join(fonts_dir, "DejaVuSans-Bold.ttf")
        font_path_italic = os.path.join(fonts_dir, "DejaVuSans-Oblique.ttf")

        if not (os.path.exists(font_path_regular) and os.path.exists(font_path_bold) and os.path.exists(font_path_italic)):
            raise FileNotFoundError("Font files are missing. Ensure DejaVuSans.ttf, DejaVuSans-Bold.ttf, and DejaVuSans-Oblique.ttf are in the fonts directory.")

        pdf.add_font("DejaVu", style="", fname=font_path_regular, uni=True)
        pdf.add_font("DejaVu", style="B", fname=font_path_bold, uni=True)
        pdf.add_font("DejaVu", style="I", fname=font_path_italic, uni=True)
        pdf.set_font("DejaVu", size=12)

        # Header
        pdf.set_font("DejaVu", size=16, style="B")
        pdf.cell(0, 10, text="Y.E TechWorld", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, text="Waar ideeën tot leven komen.", new_x="LMARGIN", new_y="NEXT", align="C")

        # Company Info
        pdf.cell(0, 10, text="Leerparkpromenade 100", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.cell(0, 10, text="3312 KW Dordrecht", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.cell(0, 10, text="Bedrijfsnummer: 06 12345678", new_x="LMARGIN", new_y="NEXT", align="C")

        # Customer Info
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
        pdf.cell(20, 10, text="Aantal", border=1)
        pdf.cell(80, 10, text="Omschrijving", border=1)
        pdf.cell(40, 10, text="Prijs/stuk", border=1)
        pdf.cell(40, 10, text="Totaal (excl. BTW)", border=1, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("DejaVu", size=10)
        for product in invoice_data["products"]:
            total = product["aantal"] * product["prijs_per_stuk_excl_btw"]
            pdf.cell(20, 10, text=str(product["aantal"]), border=1)
            pdf.cell(80, 10, text=product["productnaam"], border=1)
            pdf.cell(40, 10, text=f"\u20ac{product['prijs_per_stuk_excl_btw']:.2f}", border=1)
            pdf.cell(40, 10, text=f"\u20ac{total:.2f}", border=1, new_x="LMARGIN", new_y="NEXT")

        # Totals
        pdf.set_font("DejaVu", size=10, style="B")
        pdf.cell(140, 10, text="Totaal Exclusief BTW", border=1)
        pdf.cell(40, 10, text=f"\u20ac{invoice_data['totals']['total_excl_vat']:.2f}", border=1, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(140, 10, text="BTW", border=1)
        pdf.cell(40, 10, text=f"\u20ac{invoice_data['totals']['total_vat']:.2f}", border=1, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(140, 10, text="Totaal Inclusief BTW", border=1)
        pdf.cell(40, 10, text=f"\u20ac{invoice_data['totals']['total_incl_vat']:.2f}", border=1, new_x="LMARGIN", new_y="NEXT")

        # Footer
        pdf.set_font("DejaVu", size=10)
        pdf.cell(0, 10, text="Maak alle betalingen over aan Y.E TechWorld", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.cell(0, 10, text="Bedankt voor uw zaken.", new_x="LMARGIN", new_y="NEXT", align="C")

        pdf.output(invoice_file_path)
        print(f"✅ Created: {os.path.basename(invoice_file_path)}")

    except Exception as e:
        print(f"❌ PDF generation failed: {str(e)}")

def process_order(order_file_path, invoice_dir):
    try:
        with open(order_file_path, "r") as f:
            data = json.load(f)

        order = data.get("order", {})  # Changed from "factuur" to "order"
        
        # --- Validate required fields ---
        required_fields = {
            "klant": ["naam", "adres", "postcode", "stad", "KVK-nummer"],
            "root": ["ordernummer", "orderdatum", "betaaltermijn"]  # Changed from "factuurnummer" to "ordernummer"
        }

        # Check root-level fields
        for field in required_fields["root"]:
            if field not in order:
                raise KeyError(f"Missing root field: {field}")

        # Check customer fields
        customer = order.get("klant", {})
        for field in required_fields["klant"]:
            if field not in customer:
                raise KeyError(f"Missing customer field: {field}")

        # Check products
        products = order.get("producten", [])
        if not products:
            raise ValueError("No products found in order")

        for idx, product in enumerate(products):
            required_product_fields = ["productnaam", "aantal", "prijs_per_stuk_excl_btw"]
            for p_field in required_product_fields:
                if p_field not in product:
                    raise KeyError(f"Product {idx} missing field: {p_field}")

        # --- Rest of the processing logic ---
        total_excl_vat = sum(p["aantal"] * p["prijs_per_stuk_excl_btw"] for p in products)
        total_vat = sum(p["aantal"] * p.get("btw_percentage", 0) * p["prijs_per_stuk_excl_btw"] / 100 for p in products)
        total_incl_vat = total_excl_vat + total_vat

        invoice_data = {
            "invoice_number": order["ordernummer"],  # Changed from "factuurnummer" to "ordernummer"
            "invoice_date": order["orderdatum"],  # Changed from "factuurdatum" to "orderdatum"
            "payment_terms": order["betaaltermijn"],
            "customer": customer,
            "products": products,
            "totals": {
                "total_excl_vat": round(total_excl_vat, 2),
                "total_vat": round(total_vat, 2),
                "total_incl_vat": round(total_incl_vat, 2)
            }
        }

        pdf_path = os.path.join(invoice_dir, f"invoice_{invoice_data['invoice_number']}.pdf")
        generate_pdf(invoice_data, pdf_path)

        # Move to PROCESSED
        shutil.move(order_file_path, os.path.join(processed_dir, os.path.basename(order_file_path)))

    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"❌ Invalid order: {os.path.basename(order_file_path)} - {str(e)}")
        # Move to ERROR directory
        shutil.move(order_file_path, os.path.join(error_dir, os.path.basename(order_file_path)))
    except Exception as e:
        print(f"❌ Unexpected error: {os.path.basename(order_file_path)} - {str(e)}")
        shutil.move(order_file_path, os.path.join(error_dir, os.path.basename(order_file_path)))

# Process all JSON files
for filename in os.listdir(order_dir):
    if filename.endswith(".json"):
        process_order(os.path.join(order_dir, filename), invoice_dir)

print("✨ Processing complete!")