from PyPDF2 import PdfFileReader
import datetime as dt

REPLACEMENTS = [
    ('Œ', '-'),
    ('ﬁ', '"'),
    ('ﬂ', '"'),
    ('™', "'"),
    ('Ł', '•'),
    (',', "'"),
    ('Š', '-'),
    ('€', ' '),
    ('¬', '-'),
    ('–', '…'),
    ('‚', "'"),
    ('Ž', '™'),
    ('˚', 'fl'),
    ('˜', 'fi'),
    ('˛', 'ff'),
    ('˝', 'ffi'),
    ('š', '—'),
    ('ü', 'ti'),
    ('î', 'í'),
    ('è', 'c'),
    ('ë', 'e'),
    ('Ð', '–'),
    ('Ò', '"'),
    ('Ó', '"'),
    ('Õ', "'"),
]

class Minutes:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path
        self.reader = self.read_pdf(pdf_path)
        self.page_count = self.reader.getNumPages()
        self.date = self.parse_date(pdf_path)
        self.meeting_date = self.date.strftime("%Y-%m-%d")
        self.parsed_text = None


    def read_pdf(self, pdf_path):
        file = open(pdf_path, "rb")
        reader = PdfFileReader(file, strict=False)
        return reader


    def parse_date(self, pdf_path):
        date_str = pdf_path.stem
        date = dt.datetime.strptime(date_str, "%Y_%m_%d")
        return date


    def parse_pages(self, range_type):
        text = ""
        for page in self.reader.pages:
            text += page.extractText().strip()
        self.parsed_text = self.replace_chars(text)


    def replace_chars(self, text):
        for i in REPLACEMENTS:
            text = text.replace(i[0], i[1])
        return text
