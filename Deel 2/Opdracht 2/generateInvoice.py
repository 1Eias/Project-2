import json
from datetime import datetime
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the input JSON file
json_file_path = os.path.join(script_dir, "2000-096.json")

# Load the order data from the JSON file
with open(json_file_path, "r") as file:
    order_data = json.load(file)

# Extract relevant data from the order
order = order_data["order"]
order_number = order["ordernummer"]
order_date = order["orderdatum"]
payment_terms = order["betaaltermijn"]

# Customer details
customer = order["klant"]
customer_name = customer["naam"]
customer_address = customer["adres"]
customer_postcode = customer["postcode"]
customer_city = customer["stad"]
customer_kvk = customer["KVK-nummer"]

# Product details
products = order["producten"]

# Calculate invoice details
invoice_number = f"INV-{order_number}"  # Generate invoice number
invoice_date = datetime.today().strftime("%d-%m-%Y")  # Use today's date as invoice date

# Initialize totals
total_excl_vat = 0
total_vat = 0
total_incl_vat = 0

# Calculate totals for each product
for product in products:
    product_name = product["productnaam"]
    quantity = product["aantal"]
    price_per_unit = product["prijs_per_stuk_excl_btw"]
    vat_percentage = product["btw_percentage"]

    # Calculate total price for the product (excluding VAT)
    total_price_excl_vat = quantity * price_per_unit

    # Calculate VAT for the product
    vat_amount = total_price_excl_vat * (vat_percentage / 100)

    # Add to totals
    total_excl_vat += total_price_excl_vat
    total_vat += vat_amount
    total_incl_vat += total_price_excl_vat + vat_amount

# Round VAT amount to 2 decimal places (as per Dutch tax rules)
total_vat = round(total_vat, 2)

# Create the invoice data structure
invoice_data = {
    "invoice": {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "order_number": order_number,
        "order_date": order_date,
        "payment_terms": payment_terms,
        "customer": {
            "name": customer_name,
            "address": customer_address,
            "postcode": customer_postcode,
            "city": customer_city,
            "KVK_number": customer_kvk,
        },
        "products": products,
        "totals": {
            "total_excl_vat": round(total_excl_vat, 2),
            "total_vat": total_vat,
            "total_incl_vat": round(total_incl_vat, 2),
        },
    }
}

# Save the invoice data to a new JSON file in the script's directory
invoice_file_path = os.path.join(script_dir, "invoice_data.json")
with open(invoice_file_path, "w") as file:
    json.dump(invoice_data, file, indent=4)

print(f"Invoice JSON file has been created successfully at: {invoice_file_path}")