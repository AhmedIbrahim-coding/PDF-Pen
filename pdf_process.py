from PyPDF2 import PdfMerger


class PDF_Editor:
    def __init__(self, files):
        self.files = files

    def merge_files(self, output_path: str)  -> None:
        
        merger = PdfMerger()

        for file_path in self.files:
            merger.append(file_path)

        with open(output_path, "wb") as output_file:
            merger.write(output_file)

        merger.close()

    def split(self):
        pass

    def compress(self):
        pass