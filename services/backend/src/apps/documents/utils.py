from io import BytesIO
import zipfile


class ZipGenerator:
    @staticmethod
    def create_zip(files: dict[str, bytes]) -> bytes:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for doc_id, content in files.items():
                zip_file.writestr(f"document_{doc_id}.pdf", content)
        return zip_buffer.getvalue()