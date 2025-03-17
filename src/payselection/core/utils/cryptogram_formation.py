import base64
import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import (
    padding as padding_asymmetric,
)
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes


def encrypt_data_for_cryptogram_rsa(
    token: bytes,
    raw_pub_key: str,
) -> str:
    public_key = serialization.load_pem_public_key(
        base64.b64decode(raw_pub_key).decode().encode('utf-8'),
        backend=default_backend(),
    )

    encrypted_data = public_key.encrypt(
        token,
        padding_asymmetric.OAEP(
            mgf=padding_asymmetric.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return base64.b64encode(encrypted_data).decode('utf-8')


def encrypt_data_for_cryptogram(token: bytes, raw_pub_key: str) -> str:
    curve = ec.SECP256K1()

    pub_key = ec.EllipticCurvePublicKey.from_encoded_point(curve, bytes.fromhex(raw_pub_key))

    ephemeral_prv_key = ec.generate_private_key(ec.SECP256K1())
    ephemeral_pub_key = ephemeral_prv_key.public_key()
    raw_ephemeral_pub_key = ephemeral_pub_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )

    shared_secret = ephemeral_prv_key.exchange(ec.ECDH(), pub_key)

    hasher = hashes.Hash(hashes.SHA512())
    hasher.update(shared_secret)
    derived_key = hasher.finalize()
    aes_key, hmac_key = derived_key[:32], derived_key[32:]

    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    encryptor = Cipher(algorithms.AES(aes_key), modes.CBC(iv)).encryptor()
    ciphertext = (
        encryptor.update(padder.update(token) + padder.finalize())
        + encryptor.finalize()
    )

    signer = hmac.HMAC(hmac_key, hashes.SHA256())
    signer.update(iv)
    signer.update(raw_ephemeral_pub_key)
    signer.update(ciphertext)
    tag = signer.finalize()

    signed_message = json.dumps(
        {
            'encryptedMessage': base64.b64encode(ciphertext).decode(),
            'ephemeralPublicKey': base64.b64encode(
                raw_ephemeral_pub_key,
            ).decode(),
        },
    )

    send_data = json.dumps(
        {
            'signedMessage': signed_message,
            'iv': base64.b64encode(iv).decode(),
            'tag': base64.b64encode(tag).decode(),
        },
    )
    return base64.b64encode(send_data.encode()).decode('utf-8')
