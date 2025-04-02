import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas

# Function to merge PDFs
def merge_pdfs():
    files = filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF Files", "*.pdf")])
    if not files:
        return
    
    merger = PdfMerger()
    for pdf in files:
        merger.append(pdf)
    
    output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_filename:
        merger.write(output_filename)
        merger.close()
        messagebox.showinfo("Success", f"PDFs Merged and Saved as {output_filename}")

# Function to split a PDF
def split_pdf():
    file = filedialog.askopenfilename(title="Select PDF to Split", filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
    
    reader = PdfReader(file)
    total_pages = len(reader.pages)
    
    start_page = int(entry_start.get()) - 1
    end_page = int(entry_end.get())
    
    if start_page < 0 or end_page > total_pages or start_page >= end_page:
        messagebox.showerror("Error", "Invalid page range")
        return
    
    writer = PdfWriter()
    for i in range(start_page, end_page):
        writer.add_page(reader.pages[i])
    
    output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_filename:
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)
        messagebox.showinfo("Success", f"Pages {start_page+1} to {end_page} saved as {output_filename}")

# Function to convert text to PDF
def text_to_pdf():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "No text entered")
        return
    
    output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_filename:
        c = canvas.Canvas(output_filename)
        c.drawString(100, 750, text)
        c.save()
        messagebox.showinfo("Success", f"Text saved as {output_filename}")

# Function to extract text from a PDF
def extract_text():
    file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
    
    doc = fitz.open(file)
    extracted_text = ""
    
    for page in doc:
        extracted_text += page.get_text()
    
    text_input.delete("1.0", tk.END)
    text_input.insert("1.0", extracted_text)
    messagebox.showinfo("Success", "Text extracted from PDF")

# Create GUI
root = tk.Tk()
root.title("PDF Toolkit - I Love PDF Clone")
root.geometry("500x500")

# Buttons
tk.Button(root, text="Merge PDFs", command=merge_pdfs, width=20).pack(pady=5)
tk.Button(root, text="Split PDF", command=split_pdf, width=20).pack(pady=5)

# Split PDF Page Range
tk.Label(root, text="Start Page:").pack()
entry_start = tk.Entry(root)
entry_start.pack()
tk.Label(root, text="End Page:").pack()
entry_end = tk.Entry(root)
entry_end.pack()

tk.Button(root, text="Extract Text from PDF", command=extract_text, width=20).pack(pady=5)

# Text to PDF
text_input = tk.Text(root, height=5, width=40)
text_input.pack(pady=10)
tk.Button(root, text="Convert Text to PDF", command=text_to_pdf, width=20).pack(pady=5)

# Run App
root.mainloop()
