from fpdf import FPDF
import os

# الحصول على الدليل الذي يحتوي على السكربت
script_dir = os.path.dirname(os.path.abspath(__file__))

# تحديد مجلد الإخراج بالنسبة لمجلد السكربت
output_dir = os.path.join(script_dir, "PDF_INVOICE")

# الحصول على النص من المستخدم
user_text = input("أدخل النص الذي تريد وضعه في ملف PDF: ")

# تهيئة ملف PDF بحجم A4
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()

# تحديد الخط وموضع النص (في المنتصف)
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=user_text)

# التأكد من وجود مجلد الإخراج
os.makedirs(output_dir, exist_ok=True)

# حفظ ملف PDF
pdf.output(os.path.join(output_dir, "generated_pdf.pdf"))