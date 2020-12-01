from PyPDF2 import PdfFileReader
import datetime as dt

REPLACEMENTS = [
    ('Œ', '-'),
    ('ﬁ', '"'),
    ('ﬂ', '"'),
    ('™', "'"),
    ('Ł', '•'),
    # (',', "'"),
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

def replace_chars(text, replacement_list):
    """Replaces a set of characters specified by a list of replacement keys

    Args:
        text (str): The raw text whose characters will be replaced
        replacement_list (list): List of tuples in which the first item
        is the current character and the second item is its replacement
    Returns:
        text (str): The text with the characters replaced
    """
    for current, new in replacement_list:
        text = text.replace(current, new)
    return text

class Minutes:
    """Creates an object that represents the minutes for an individual BOE
    meeting. This object contains the methods used to parse the pdf and
    stores the outputs of that parsing as a set of attributes"""

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path
        self.reader = self.read_pdf(pdf_path)
        self.page_count = self.reader.getNumPages()
        self.date = self.parse_date(pdf_path)
        self.meeting_date = self.date.strftime("%Y-%m-%d")
        self.parsed_text = None


    def read_pdf(self, pdf_path):
        """Initializes a PdfFileReader instance from the PyPDF2 library that
        will be called in subsequent methods and attributes

        Args:
            pdf_path (pathlib.Path): The path to the pdf file to read
        Returns:
            reader (PyPDF2.PdfFileReader): Returns an instance of PdfFileReader
            that will be stored in self.reader
        """
        file = open(pdf_path, "rb")
        reader = PdfFileReader(file, strict=False)
        return reader


    def parse_date(self, pdf_path):
        """Parses a datetime object from the path to the pdf file for use
        in self.meeting_date and self.year

        Args:
            pdf_path (pathlib.Path): Path to minutes file passed during
            instantiation of the Minutes class, expected to end with a
            */YYYY_MM_DD.pdf pattern
        Returns:
            date (datetime.datetime): Returns a datetime object of the
            date parsed from the pdf_path that will be stored in self.date
        """
        date_str = pdf_path.stem
        date = dt.datetime.strptime(date_str, "%Y_%m_%d")
        return date


    def parse_pages(self):
        """Extracts text from pdf pages and stores it in self.parsed_text

        Args:
            self: Uses the self.reader object created by self.read_pdf()
        Returns:
            text (str): Returns the text parsed from the pdf pages as a string
            and also stores that text in self.parsed_text
        """
        text_raw = ""
        for page in self.reader.pages:
            text_raw += page.extractText().strip()
        text = replace_chars(text_raw, REPLACEMENTS)
        self.parsed_text = text
        return text
