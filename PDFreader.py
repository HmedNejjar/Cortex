from pypdf import PdfReader
from pathlib import Path
from typing import List

def readPDF(file_path: str | Path) -> dict:
    """Read and extract text from a PDF file.
    
    Args:
        file_path: Path to the PDF file (string or Path object)
        
    Returns:
        Dictionary containing:
            - file_name: Name of the PDF file
            - num_pages: Total number of pages
            - pages: List of text extracted from each page
            - full_text: All text concatenated together
            
    Raises:
        PDFReadError: If file not found, not a PDF, or extraction fails
    """
    # Convert file path to Path object for better path handling
    path = Path(file_path)
    
    if not path.exists():
        raise PDFReadError(f"File not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise PDFReadError("File is not a PDF")

    try:
        reader = PdfReader(path)
    except Exception as e:
        raise PDFReadError(f"Failed to open PDF: {e}")
    
    # Initialize list to store text from each page
    pages_text: List[str] = []
    
    # Iterate through each page and extract text
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
        except Exception as e:
            raise PDFReadError(f"Failed to extract text from page {i}: {e}")
        
        if text is None:
            text = ""
        
        # Clean up text: remove carriage returns and strip whitespace
        text = text.replace("\r", "").strip()
        
        pages_text.append(text)
        
    # Combine all pages with double newlines for readability
    full_text = "\n\n".join(pages_text)

    return {"file_name": path.name,
            "num_pages": len(pages_text),
            "pages": pages_text,
            "full_text": full_text
            }


class PDFReadError(Exception):
    """Custom exception raised for PDF reading and processing errors."""
    pass