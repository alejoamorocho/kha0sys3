import docx

def extract_text(filename):
    print(f"--- START OF {filename} ---")
    try:
        doc = docx.Document(filename)
        for para in doc.paragraphs:
            print(para.text)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    print(f"--- END OF {filename} ---")

extract_text('c:\\Proyectos\\kha0sys3\\ORB_Framework_Evaluacion.docx')
extract_text('c:\\Proyectos\\kha0sys3\\ORB_Pseudocodigo_Engine.docx')
