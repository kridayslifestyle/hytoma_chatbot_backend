from pypdf import PdfReader
from docx import Document


def load_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        text += page.extract_text()

    return text




def load_docx(path):

    doc = Document(path)

    text = ""

    for p in doc.paragraphs:

        text += p.text + "\n"

    return text