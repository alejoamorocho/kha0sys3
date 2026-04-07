import docx
import sys

def extract_text(filename, out_file):
    out_file.write(f"--- START OF {filename} ---\n")
    try:
        doc = docx.Document(filename)
        for para in doc.paragraphs:
            out_file.write(para.text + "\n")
    except Exception as e:
        out_file.write(f"Error reading {filename}: {e}\n")
    out_file.write(f"--- END OF {filename} ---\n")

with open('c:\\Proyectos\\kha0sys3\\extract_utf8.txt', 'w', encoding='utf-8') as f:
    extract_text('c:\\Proyectos\\kha0sys3\\ORB_Framework_Evaluacion.docx', f)
    extract_text('c:\\Proyectos\\kha0sys3\\ORB_Pseudocodigo_Engine.docx', f)
