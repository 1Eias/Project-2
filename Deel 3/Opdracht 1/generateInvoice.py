from fpdf import FPDF
import json
import os

# الحصول على مسار المجلد الحالي
script_dir = os.path.dirname(os.path.abspath(__file__))

# مسار ملف JSON
json_file_path = os.path.join(script_dir, "invoice_data.json")

# قراءة البيانات من ملف JSON
with open(json_file_path, "r") as file:
    invoice_data = json.load(file)

# استخراج البيانات
invoice = invoice_data["invoice"]
customer = invoice["customer"]
products = invoice["products"]
totals = invoice["totals"]

# إنشاء ملف PDF
pdf = FPDF()
pdf.add_page()

# إضافة خط يدعم الرموز Unicode (مثال: DejaVu Sans)
# إضافة الخطوط مع المسار الكامل
pdf.add_font(
    "DejaVuSans", 
    "", 
    os.path.join(script_dir, "DejaVuSans.ttf")
)
pdf.add_font(
    "DejaVuSans", 
    "B", 
    os.path.join(script_dir, "DejaVuSans-Bold.ttf")
)
pdf.add_font(
    "DejaVuSans", 
    "I", 
    os.path.join(script_dir, "DejaVuSans-Oblique.ttf")
)

# إضافة العنوان
pdf.set_font("DejaVuSans", size=16, style='B')
pdf.cell(0, 10, text="Y.E TechWorld", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.set_font("DejaVuSans", size=12, style='I')
pdf.cell(0, 10, text="Waar ideeën tot leven komen.", new_x="LMARGIN", new_y="NEXT", align='C')

# معلومات الشركة
pdf.set_font("DejaVuSans", size=10)
pdf.cell(0, 10, text="Leerparkpromenade 100", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 10, text="3312 KW Dordrecht", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 10, text="Bedrijfsnummer: 06 12345678", new_x="LMARGIN", new_y="NEXT", align='C')

# قسم العميل
pdf.set_font("DejaVuSans", size=12, style='B')
pdf.cell(0, 10, text="Factuur voor:", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.set_font("DejaVuSans", size=10)
pdf.cell(0, 10, text=f"Naam: {customer['name']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"Bedrijfsnaam: {customer['name']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"Adres: {customer['address']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"Postcode: {customer['postcode']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"Stad: {customer['city']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"KVK-nummer: {customer['KVK_number']}", new_x="LMARGIN", new_y="NEXT", align='L')

# تفاصيل الفاتورة
pdf.set_font("DejaVuSans", size=12, style='B')
pdf.cell(0, 10, text=f"Factuurnummer: {invoice['invoice_number']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"Factuurdatum: {invoice['invoice_date']}", new_x="LMARGIN", new_y="NEXT", align='L')
pdf.cell(0, 10, text=f"Betaaltermijn: {invoice['payment_terms']}", new_x="LMARGIN", new_y="NEXT", align='L')

# الجدول
pdf.set_font("DejaVuSans", size=10, style='B')
pdf.cell(20, 10, text="Aantal", border=1, align='C')
pdf.cell(80, 10, text="Omschrijving", border=1, align='C')
pdf.cell(40, 10, text="Prijs", border=1, align='C')
pdf.cell(40, 10, text="Prijs (excl. BTW)", border=1, align='C', new_x="LMARGIN", new_y="NEXT")

# إضافة المنتجات
for product in products:
    pdf.cell(20, 10, text=str(product["aantal"]), border=1, align='C')
    pdf.cell(80, 10, text=product["productnaam"], border=1, align='C')
    pdf.cell(40, 10, text=f"€{product['prijs_per_stuk_excl_btw']:.2f}", border=1, align='C')
    pdf.cell(40, 10, text=f"€{product['aantal'] * product['prijs_per_stuk_excl_btw']:.2f}", border=1, align='C', new_x="LMARGIN", new_y="NEXT")

# التذييل
pdf.set_font("DejaVuSans", size=10, style='B')
pdf.cell(140, 10, text="Totaal Exclusief BTW", border=1, align='R')
pdf.cell(40, 10, text=f"€{totals['total_excl_vat']:.2f}", border=1, align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(140, 10, text="BTW Percentage (21%)", border=1, align='R')
pdf.cell(40, 10, text=f"€{totals['total_vat']:.2f}", border=1, align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(140, 10, text="Totaal", border=1, align='R')
pdf.cell(40, 10, text=f"€{totals['total_incl_vat']:.2f}", border=1, align='C', new_x="LMARGIN", new_y="NEXT")

# نص الشكر
pdf.set_font("DejaVuSans", size=10)
pdf.cell(0, 10, text="Maak alle betalingen over aan Y.E TechWorld", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 10, text="Als u vragen heeft over deze factuur, neem dan contact op met [Naam, telefoon, e-mail]", new_x="LMARGIN", new_y="NEXT", align='C')
pdf.cell(0, 10, text="Bedankt voor uw zaken.", new_x="LMARGIN", new_y="NEXT", align='C')

# حفظ الملف
output_dir = os.path.join(script_dir, "PDF_INVOICE")
os.makedirs(output_dir, exist_ok=True)
pdf.output(os.path.join(output_dir, "invoice.pdf"))

print("The PDF_INVOICE has been created!")