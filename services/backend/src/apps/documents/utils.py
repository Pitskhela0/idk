from io import BytesIO
import zipfile
import base64
from typing import Optional


def encode_base64(content: bytes) -> str:
    return base64.b64encode(content).decode('utf-8')


def create_zip_archive(files: dict[str, bytes]) -> bytes:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for doc_id, content in files.items():
            zip_file.writestr(f"document_{doc_id}.pdf", content)
    return zip_buffer.getvalue()
