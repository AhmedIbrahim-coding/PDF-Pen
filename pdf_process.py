from PyPDF2 import PdfMerger, PdfWriter, PdfReader
import os
import io


class PDF_Editor:
    def __init__(self, files):
        self.files = files
        self.edited_files = 0

    def merge_files(self, output_path: str, temp: bool = False):
        
        merger = PdfMerger()

        for file_path in self.files:
            merger.append(file_path)

        if temp:
            temp_buffer = io.BytesIO()
            merger.write(temp_buffer)
            merger.close()
            temp_buffer.seek(0)
            return temp_buffer
        else:
            with open(output_path, "wb") as output_file:
                merger.write(output_file)

            merger.close()

    def split(self, output_path: str, split_range: int) -> None:

        # first we have to merge all files into one temporary file
        reader = PdfReader(self.merge_files(output_path, temp=True))

        # then slice the merged files into small files
        total_pages = len(reader.pages)
        for start in range(0, total_pages, split_range):
            writer = PdfWriter()

            for i in range(start, min(start+split_range, total_pages)):
                writer.add_page(reader.pages[i])

            output_name = os.path.join(output_path, f"{start+1}_{min(start+split_range, total_pages)}.pdf")
            with open(output_name, "wb") as f:
                writer.write(f)


    def compress(self, output_path: str):
        self.edited_files = 0
        for file in self.files: 
            reader = PdfReader(file)
            writer = PdfWriter()

            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)

            file_name = os.path.basename(file)
            final_path = os.path.join(output_path, file_name)
            with open(final_path, "wb") as compressor:
                writer.write(compressor)

            self.edited_files += 1
            print(self.edited_files)