import PyPDF2
from PyPDF2 import PdfFileReader

class Extractpdf:

    def __init__(self, file, pgno):
        
        self.file = file
        self.pgno = pgno

    # def extract_information(pdf_path):
    #     with open(pdf_path, 'rb') as f:
    #         pdf = PdfFileReader(f)
    #         information = pdf.getDocumentInfo()
    #         number_of_pages = pdf.getNumPages()

    #     txt = f""" 
    #     Information about {pdf_path}: 

    #     Author: {information.author}
    #     Creator: {information.creator}
    #     Producer: {information.producer}
    #     Subject: {information.subject}
    #     Title: {information.title}
    #     Number of pages: {number_of_pages}
    #     """

    #     print(txt)
    #     return information
    def read_content(self):
        # creating a pdf reader object
        reader = PyPDF2.PdfReader(self.file)
        text = reader.pages[int(self.pgno)-1].extract_text()
        return text

