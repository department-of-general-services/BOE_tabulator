from PyPDF2 import PdfFileReader
import datetime as dt

class Minutes:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path
        self.reader = self.read_pdf(pdf_path)
        self.page_count = self.reader.getNumPages()
        self.date = self.parse_date(pdf_path)
        self.meeting_date = self.date.strftime("%Y-%m-%d")


    def read_pdf(self, pdf_path):
        file = open(pdf_path, "rb")
        reader = PdfFileReader(file, strict=False)
        return reader

    def parse_date(self, pdf_path):
        date_str = pdf_path.stem
        date = dt.datetime.strptime(date_str, "%Y_%m_%d")
        return date
