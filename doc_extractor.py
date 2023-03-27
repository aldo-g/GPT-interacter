import docx
import os


def read_docx(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return ""
    
    doc = docx.Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)