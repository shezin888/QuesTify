import PyPDF2

def extract_text(pdf_path, start_page, end_page):
    """
    Extracts text from pages `start_page` to `end_page` of a PDF file at `pdf_path`.
    Returns a string containing the extracted text.
    """
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        if end_page > pdf_reader.getNumPages():
            end_page = pdf_reader.getNumPages()
        text = ''
        for i in range(start_page-1, end_page):
            page = pdf_reader.getPage(i)
            text += page.extractText()
        return text

# Example usage
pdf_path = '/home/shezin/Desktop/question_generator/4_1 Wearable Computing and Sensor Systems for Healthcare-1.pdf'
start_page = 1
end_page = 3
text = extract_text(pdf_path, start_page, end_page)
print(text)