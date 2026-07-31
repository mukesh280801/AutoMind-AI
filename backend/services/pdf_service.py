import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    """

    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:
        full_text += page.get_text()

    document.close()

    return full_text