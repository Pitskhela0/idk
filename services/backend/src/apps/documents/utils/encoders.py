import base64


class Base64Encoder:
    @staticmethod
    def encode_base64(content: bytes) -> str:
        return base64.b64encode(content).decode('utf-8')
