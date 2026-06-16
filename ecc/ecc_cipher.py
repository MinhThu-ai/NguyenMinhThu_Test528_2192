from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import os


class ECCCipher:
    def __init__(self):
        self.keys_folder = "keys"
        self.private_key_path = os.path.join(self.keys_folder, "private_key.pem")
        self.public_key_path = os.path.join(self.keys_folder, "public_key.pem")

        if not os.path.exists(self.keys_folder):
            os.makedirs(self.keys_folder)

    def generate_keys(self):
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        with open(self.private_key_path, "wb") as private_file:
            private_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        with open(self.public_key_path, "wb") as public_file:
            public_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

        return "ECC keys generated successfully"

    def load_private_key(self):
        with open(self.private_key_path, "rb") as private_file:
            private_key = serialization.load_pem_private_key(
                private_file.read(),
                password=None
            )

        return private_key

    def load_public_key(self):
        with open(self.public_key_path, "rb") as public_file:
            public_key = serialization.load_pem_public_key(
                public_file.read()
            )

        return public_key

    def sign(self, message):
        if not os.path.exists(self.private_key_path):
            self.generate_keys()

        private_key = self.load_private_key()

        signature = private_key.sign(
            message.encode("utf-8"),
            ec.ECDSA(hashes.SHA256())
        )

        return signature.hex()

    def verify(self, message, signature):
        if not os.path.exists(self.public_key_path):
            return False

        public_key = self.load_public_key()

        try:
            public_key.verify(
                bytes.fromhex(signature),
                message.encode("utf-8"),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False