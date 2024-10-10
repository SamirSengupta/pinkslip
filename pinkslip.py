import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import sys

def add_hidden_text_to_pdf(input_pdf_path, output_pdf_path, hidden_text):
    # Read the existing PDF
    with open(input_pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Create a new PDF with the hidden text
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Adding the hidden text (white font color, font size 1)
        can.setFont("Helvetica", 1)
        can.setFillColor(colors.white)

        # Position text at the beginning of the next line (bottom left corner)
        x_position = 100  # You can adjust this value for positioning
        y_position = 750  # Adjust depending on the PDF content

        can.drawString(x_position, y_position, hidden_text)
        can.save()

        packet.seek(0)
        hidden_text_pdf = PyPDF2.PdfReader(packet)

        # Create a PDF writer to save the final PDF
        pdf_writer = PyPDF2.PdfWriter()

        # Add the hidden text to each page
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            hidden_text_page = hidden_text_pdf.pages[0]
            
            # Merge the hidden text PDF with the original page
            page.merge_page(hidden_text_page)
            pdf_writer.add_page(page)

        # Save the new PDF
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

if __name__ == "__main__":
    # Ask user for the file name
    input_pdf = input("Enter the full path of the PDF file (including the file name): ")
    output_pdf = input_pdf.replace(".pdf", "_updated.pdf")
    
    # Ask user for multi-line hidden text
    print("Enter the text you want to hide in the PDF (end input with Ctrl+D for Unix/Linux or Ctrl+Z for Windows):")
    hidden_text = sys.stdin.read()  # This will read until EOF

    add_hidden_text_to_pdf(input_pdf, output_pdf, hidden_text)
    print(f"Updated PDF saved as {output_pdf}")
