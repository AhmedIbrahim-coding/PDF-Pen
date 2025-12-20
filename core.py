from pdf_process import PDF_Editor

def merge_files(files: list[str], output_path: str)  -> None:
    
    editor = PDF_Editor(files)
    editor.merge_files(output_path)
