from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
import io
import re 

def fill_pdf(input_pdf_path, output_pdf_path, field_positions, letter_spacing=0):
    # Register DejaVuSans font with ReportLab
    pdfmetrics.registerFont(TTFont('ArialR', 'BAHNSCHRIFT.ttf'))

    # Create a new PDF to overlay the data
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Set the font to DejaVuSans
    can.setFont("ArialR", 12)

    # Dictionary to store filled values
    filled_values = {}

     # Define the length of the account number field
    NR_RACHUNKU_LENGTH = 26

    # Fill the form with the provided data
    for field_name, (x, y) in field_positions.items():
        # If this field is one of the "2" fields and its corresponding field has been filled
        if field_name.endswith("2") and field_name[:-1] in filled_values:
            field_value = filled_values[field_name[:-1]]
        else:
            field_value = input(f"Enter value for {field_name}: ")
            # Store the value for future reference
            filled_values[field_name] = field_value
        if field_name.startswith("Nr rachunku odbiorcy"):
            field_value = format_account_number(field_value)


        # Draw the text with custom letter spacing if not in specific fields
        if field_name not in ["Nazwa odbiorcy cd.", "Numer rachunku zleceniodawcy/kwota słownie", "Nazwa odbiorcy cd.2", "Numer rachunku zleceniodawcy/kwota słownie2","Nazwa zleceniowdawcy cd","Nazwa zleceniowdawcy cd2", "Nr rachunku odbiorcy", "Nr rachunku odbiorcy2"]:
            draw_text_with_spacing(can, x, y, field_value, letter_spacing)
        else:
            can.drawString(x, y, field_value)

    can.save()

    # Move to the beginning of the BytesIO buffer
    packet.seek(0)
    
    # Read the existing PDF
    existing_pdf = PdfReader(input_pdf_path)
    new_pdf = PdfReader(packet)
    
    output = PdfWriter()
    
    # Merge the new PDF with the existing PDF
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        if i == 0:
            page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # Write the output to a new PDF
    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)

def draw_text_with_spacing(can, x, y, text, letter_spacing):
    # Draw each character with specified spacing
    for char in text:
        can.drawString(x, y, char)
        x += can.stringWidth(char) + letter_spacing

def format_account_number(account_number):
    # Format account number with spaces every two characters
    return re.sub(r"(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", r"\1   \2   \3  \4   \5   \6   \7  \8   \9   \10   \11  \12   \13  \14   \15  \16  \17   \18   \19   \20   \21  \22   \23   \24  \25  \26", account_number)

if __name__ == "__main__":
    # Path to the input and output PDFs
    input_pdf_path = "druk-przelewu-podatku.pdf"
    output_pdf_path = "wypelniony-druk-przelewu.pdf"

    # Field positions in the PDF
    field_positions = {
        "Nazwa odbiorcy": (105, 780),
        "Nazwa odbiorcy cd.": (105, 756),
        "Nr rachunku odbiorcy": (105, 731),
        "Kwota cyfry": (320, 708),
        "Numer rachunku zleceniodawcy/kwota słownie": (105, 683),
        "Nazwa zleceniowdawcy": (105, 658),
        "Nazwa zleceniowdawcy cd": (105, 634),
        "Tytułem": (105, 610),
        "Tytułem cd": (105, 586),
        "Nazwa odbiorcy2" : (105, 469),
        "Nazwa odbiorcy cd.2": (105, 445),
        "Nr rachunku odbiorcy2": (105, 421),
        "Kwota cyfry2": (320, 397),
        "Numer rachunku zleceniodawcy/kwota słownie2": (105, 373),
        "Nazwa zleceniowdawcy2": (105, 348),
        "Nazwa zleceniowdawcy cd2": (105, 324),
        "Tytułem2": (105, 299),
        "Tytułem cd2": (105, 275),
        # Add more fields as needed
    }

    # Adjust the letter spacing here (in points)
    letter_spacing = 9  # For example, 9 points

    fill_pdf(input_pdf_path, output_pdf_path, field_positions, letter_spacing)
