from pdf_process import PDF_Editor

def merge_files(files: dict, output_path: str)  -> None:
    
    editor = PDF_Editor(list(files.values()))
    editor.merge_files(output_path)

def split_files(file:dict, output_path:str, split_range) -> None:

    editor = PDF_Editor(list(file.values()))
    editor.split(output_path, split_range)


class EntryError(Exception):
    pass
