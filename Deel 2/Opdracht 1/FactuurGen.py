from fpdf import FPDF
import os

# الحصول على الدليل الذي يحتوي على السكربت
script_dir = os.path.dirname(os.path.abspath(__file__))

# تحديد مجلد الإخراج بالنسبة لمجلد السكربت
output_dir = os.path.join(script_dir, "PDF_INVOICE")

# تهيئة ملف PDF بحجم A4
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()

# إضافة العنوان
pdf.set_font("Arial", size=16, style='B')
pdf.cell(0, 10, txt="Y.E TechWorld", ln=True, align='C')
pdf.set_font("Arial", size=12, style='I')
pdf.cell(0, 10, txt="Waar ideeën tot leven komen.", ln=True, align='C')

# إضافة معلومات الشركة
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, txt="Leerparkpromenade 100", ln=True, align='C')
pdf.cell(0, 10, txt="3312 KW Dordrecht", ln=True, align='C')
pdf.cell(0, 10, txt="Bedrijfsnummer: 06 12345678", ln=True, align='C')

# إضافة قسم العميل
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Factuur voor:", ln=True, align='L')
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, txt="Naam:", ln=True, align='L')
pdf.cell(0, 10, txt="Bedrijfsnaam:", ln=True, align='L')
pdf.cell(0, 10, txt="Adres:", ln=True, align='L')
pdf.cell(0, 10, txt="Telefoonnummer:", ln=True, align='L')

# إضافة قسم الملاحظات
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Opmerkingen:", ln=True, align='L')

# إضافة قسم الفاتورة
pdf.set_font("Arial", size=12, style='B')
pdf.cell(0, 10, txt="Factuurnummer:", ln=True, align='L')
pdf.cell(0, 10, txt="Datum:", ln=True, align='L')

# إضافة الجدول
pdf.set_font("Arial", size=10, style='B')
pdf.cell(20, 10, txt="Aantal", border=1, align='C')
pdf.cell(80, 10, txt="Omschrijving", border=1, align='C')
pdf.cell(40, 10, txt="Prijs", border=1, align='C')
pdf.cell(40, 10, txt="Prijs (excl. BTW)", border=1, align='C', ln=True)

# إضافة صفوف فارغة للجدول
for _ in range(10):
    pdf.cell(20, 10, txt="", border=1, align='C')
    pdf.cell(80, 10, txt="", border=1, align='C')
    pdf.cell(40, 10, txt="", border=1, align='C')
    pdf.cell(40, 10, txt="", border=1, align='C', ln=True)

# إضافة التذييل مع خلايا محددة
pdf.set_font("Arial", size=10, style='B')
pdf.cell(140, 10, txt="Totaal Exclusief BTW", border=1, align='R')
pdf.cell(40, 10, txt="", border=1, ln=True)  # Empty cell for alignment
pdf.cell(140, 10, txt="BTW Percentage (21%)", border=1, align='R')
pdf.cell(40, 10, txt="", border=1, ln=True)  # Empty cell for alignment
pdf.cell(140, 10, txt="Totaal", border=1, align='R')
pdf.cell(40, 10, txt="", border=1, ln=True)  # Empty cell for alignment

# إضافة نص الشكر
pdf.set_font("Arial", size=10)
pdf.cell(0, 10, txt="Maak alle betalingen over aan Y.E TechWorld", ln=True, align='C')
pdf.cell(0, 10, txt="Als u vragen heeft over deze factuur, neem dan contact op met [Naam, telefoon, e-mail]", ln=True, align='C')
pdf.cell(0, 10, txt="Bedankt voor uw zaken.", ln=True, align='C')

# التأكد من وجود مجلد الإخراج
os.makedirs(output_dir, exist_ok=True)

# حفظ ملف PDF
pdf.output(os.path.join(output_dir, "factuur_template.pdf"))