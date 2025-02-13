# -*- coding: utf-8 -*-
"""Secure_Programming-Assignment_4.ipynb

## **ASSIGMENT INSTRUCTIONS**
Using Colaboratory tool, Python language, and pyca/pycryptodome or pyca/cryptography libraries (or both), do:

Choose a file 1 MB approximately, from now on, this file will be known as "original file".

Generate hashes MD5, SHA-1, SHA-2 and SHA-3 for original file.

Encrypt the file using AES-128-CTR and measure elapsed time to encrypt it.

Encrypt the file using RSA with 2048 key length and measure elapsed time to
encrypt it.

Generate hashes MD5, SHA-1, SHA-2 and SHA-3 for the encrypted files (AES and RSA).

Decrypt the file using AES-128-CTR and measure elapsed time to decrypt it.

Decrypt the file using RSA with its respective private key and measure elapsed time to decrypt it.

Generate again MD5, SHA-1, SHA-2 and SHA-3 hashes for each decrypted file and compare them with hashes from original file.

Sign the encrypted AES file with ECDSA and verify the signature.

Write a report which includes evidence (screenshots), the link to your Colab project and explain why symmetric-key encryption is faster than public-key encryption algorithms used.

Submit the report to this assignment.

Note: You can pick examples from internet, but you must reference them on your report. Plagiarism between teams will be penalized.

# **IMPORTS**
"""

# Installa la API necesaria:
#!pip install cryptography

import os
import timeit
import base64
from sys import getsizeof
from google.colab import files
from timeit import default_timer as timer
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import ec

# Para archivos de texto (.txt):
# ruta = "/content/Secure_Test.txt"
# with open(ruta, 'rb') as textFile:
#     file = textFile.read()

# Para imágenes (preferible usar .png):
ruta = "/content/images/logo_png.png"
with open(ruta, "rb") as image:
    file = base64.b64encode(image.read())

"""# **HASHING**


---

## MD5
"""


def digest_MD5(file):
    digest = hashes.Hash(hashes.MD5())
    digest.update(file)
    return digest.finalize()


"""## SHA-1"""


def digest_SHA1(file):
    digest = hashes.Hash(hashes.SHA1())
    digest.update(file)
    return digest.finalize()


"""## SHA-2"""


def digest_SHA2_256(file):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(file)
    return digest.finalize()


"""## SHA-3-256"""


def digest_SHA3_256(file):
    digest = hashes.Hash(hashes.SHA3_256())
    digest.update(file)
    return digest.finalize()


"""## Function to compare two lists of digests"""


# Verifica que dos hashes sean iguales e imprime true si eso sucede:
def compare_hashes(digests1, digests2):
    if len(digests1) != len(digests2):
        print(False)
        return

    # Si ambas listas tienen la misma cantidad de elementos se comparan:
    for digest in digests1:
        if digest not in digests2:
            print(False)
            return

    print(True)
    return


"""# **ENCRYPTING**

---

## ENCRYPT with AES-128-CTR
"""


def encrypt_AES_128_CTR(file, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(file) + encryptor.finalize()
    return (ciphertext, iv)


"""## DECRYPT with AES-128-CTR"""


def decrypt_AES_128_CTR(cipher_text, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(cipher_text) + decryptor.finalize()


"""## AES-128-CTR test"""

# Se genera la clave:
key = os.urandom(32)

# Se encripta:
ciphertext, iv = encrypt_AES_128_CTR(file, key)

# Se desencripta:
message = decrypt_AES_128_CTR(ciphertext, key, iv)

# Se comprueba que el mensaje original y el nuevo mensaje sean iguales:
file == message
print(type(message))

# Se genera el archivo a partir del mensaje decodificado:
decodeit = open("/content/mensaje_AES_dec.txt", "wb")
decodeit.write(message)
decodeit.close()

# Se genera la imagen a partir del mensaje decodificado:
"""
decodeit = open("/content/mensaje_AES_dec.png", 'wb')
decodeit.write(base64.b64decode(message))
decodeit.close()
"""

"""## Generating HASHES of AES-128-CTR encrypted and decrypted texts"""

# Archivo original sin encriptar:
orgF_md5 = digest_MD5(file)
orgF_sha1 = digest_SHA1(file)
orgF_sha2 = digest_SHA2_256(file)
orgF_sha3 = digest_SHA3_256(file)

orgF_digests = [orgF_md5, orgF_sha1, orgF_sha2, orgF_sha3]

print("The digests of the original file are: ")
print("MD5:       " + str(orgF_md5))
print("SHA-1:     " + str(orgF_sha1))
print("SHA-2_256: " + str(orgF_sha2))
print("SHA-3_256: " + str(orgF_sha3) + "\n\n")

# Encriptado:
cipher_md5 = digest_MD5(ciphertext)
cipher_sha1 = digest_SHA1(ciphertext)
cipher_sha2 = digest_SHA2_256(ciphertext)
cipher_sha3 = digest_SHA3_256(ciphertext)

print("The digests of the encrypted file are: ")
print("MD5:       " + str(cipher_md5))
print("SHA-1:     " + str(cipher_sha1))
print("SHA-2_256: " + str(cipher_sha2))
print("SHA-3_256: " + str(cipher_sha3) + "\n\n")

# Desencriptado:
message_md5 = digest_MD5(message)
message_sha1 = digest_SHA1(message)
message_sha2 = digest_SHA2_256(message)
message_sha3 = digest_SHA3_256(message)

message_digests = [message_md5, message_sha1, message_sha2, message_sha3]

print("The digests of the decrypted file are: ")
print("MD5:       " + str(message_md5))
print("SHA-1:     " + str(message_sha1))
print("SHA-2_256: " + str(message_sha2))
print("SHA-3_256: " + str(message_sha3) + "\n\n")

# Se comparan todos los hashes del archivo original con los del mensaje desencriptado:
print(
    "All the digests of the original file and the decrypted file are the same", end=": "
)
compare_hashes(orgF_digests, message_digests)

"""## ENCRYPT with RSA with a KEY of 2048"""


def encrypt_RSA(file, public_key):
    ciphertext = public_key.encrypt(
        file,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


"""## DECRYPT with RSA with a KEY of 2048"""


def decrypt_RSA(ciphertext, private_key):
    message = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return message


"""## RSA test"""


# Automatiza la generación de pedazos de una cadena de bytes, retorna una lista con los pedazos:
def chunk(b_string):
    return [b_string[i : i + 100] for i in range(0, len(b_string), 100)]


# Se generan las claves pública y privada:
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Se obtiene la lista con los pedazos de la cadena de bytes:
lstStr = chunk(file)

d_message = []
message = b""

# Se van iterando los pedazos de cadena:
for b_str in lstStr:
    # Se encripta:
    ciphertext = encrypt_RSA(b_str, public_key)

    # Se desencripta:
    d_message.append(decrypt_RSA(ciphertext, private_key))

message = b"".join(d_message)

# Se comprueba que el mensaje original y el nuevo mensaje sean iguales:
print(file == message)

# Se genera el archivo a partir del mensaje decodificado:
# decodeit = open("/content/mensaje_RSA_dec.txt", 'wb')
# decodeit.write(message)
# decodeit.close()

# Se genera la imagen a partir del mensaje decodificado:
decodeit = open("/content/mensaje_RSA_dec.png", "wb")
decodeit.write(base64.b64decode(message))
decodeit.close()

"""## Generating HASHES of RSA encrypted and decrypted texts"""

# Archivo original sin encriptar:
orgF_md5 = digest_MD5(file)
orgF_sha1 = digest_SHA1(file)
orgF_sha2 = digest_SHA2_256(file)
orgF_sha3 = digest_SHA3_256(file)

orgF_digests = [orgF_md5, orgF_sha1, orgF_sha2, orgF_sha3]

print("The digests of the original file are: ")
print("MD5:       " + str(orgF_md5))
print("SHA-1:     " + str(orgF_sha1))
print("SHA-2_256: " + str(orgF_sha2))
print("SHA-3_256: " + str(orgF_sha3) + "\n\n")

# Encriptado:
cipher_md5 = digest_MD5(ciphertext)
cipher_sha1 = digest_SHA1(ciphertext)
cipher_sha2 = digest_SHA2_256(ciphertext)
cipher_sha3 = digest_SHA3_256(ciphertext)

print("The digests of the encrypted file are: ")
print("MD5:       " + str(cipher_md5))
print("SHA-1:     " + str(cipher_sha1))
print("SHA-2_256: " + str(cipher_sha2))
print("SHA-3_256: " + str(cipher_sha3) + "\n\n")

# Desencriptado:
message_md5 = digest_MD5(message)
message_sha1 = digest_SHA1(message)
message_sha2 = digest_SHA2_256(message)
message_sha3 = digest_SHA3_256(message)

message_digests = [message_md5, message_sha1, message_sha2, message_sha3]

print("The digests of the decrypted file are: ")
print("MD5:       " + str(message_md5))
print("SHA-1:     " + str(message_sha1))
print("SHA-2_256: " + str(message_sha2))
print("SHA-3_256: " + str(message_sha3) + "\n\n")

# Se comparan todos los hashes del archivo original con los del mensaje desencriptado:
print(
    "All the digests of the original file and the decrypted file are the same", end=": "
)
compare_hashes(orgF_digests, message_digests)

"""# **SIGNING a text**

## Signing a text with RSA
"""


# Firma un mensaje:
def signText_RSA(message, chosen_hash, private_key):

    signature = private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(chosen_hash), salt_length=padding.PSS.MAX_LENGTH),
        chosen_hash,
    )

    return signature


"""## Verifying a signature with RSA"""


# Valida la firma del mensaje, retorna True o False (además imprime el mensaje de error).
def verifySign_RSA(message, signature, chosen_hash, public_key):
    try:
        verification = public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(chosen_hash), salt_length=padding.PSS.MAX_LENGTH
            ),
            chosen_hash,
        )
        return True
    except cryptography.exceptions.InvalidSignature as error:
        print("ERROR: Failed signature verification.\n")
        return False


"""### Testing signing-verification with RSA"""

# Se generan las claves pública y privada:
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Se obtiene el digest:
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash)
hasher.update(file)
digest = hasher.finalize()

# Se firma el digest:
signature = signText_RSA(digest, chosen_hash, private_key)
print("Digest:    " + str(digest))
print("Signature: " + str(signature))

# Se verifica la firma del digest:
print("The signature is the same", end=": ")
print(verifySign_RSA(digest, signature, chosen_hash, public_key))

"""## Signing a text with ECDSA"""


# Firma un mensaje:
def signText_ECDSA(message, private_key, chosen_hash):
    signature = private_key.sign(message, ec.ECDSA(chosen_hash))

    return signature


"""## Verifying a text with ECDSA"""


# Valida la firma del mensaje, retorna True o False (además imprime el mensaje de error).
def verifySign_ECDSA(message, signature, chosen_hash, public_key):
    try:
        verification = public_key.verify(signature, message, ec.ECDSA(chosen_hash))
        return True
    except cryptography.exceptions.InvalidSignature as error:
        print("ERROR: Failed signature verification.\n")
        return False


"""### Testing signing-verification with ECDSA"""

# Se crean las claves privada y pública:
private_key = ec.generate_private_key(ec.SECP384R1())
public_key = private_key.public_key()

# Se obtiene el digest:
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash)
hasher.update(file)
digest = hasher.finalize()

# Se firma el digest:
signature = signText_ECDSA(digest, private_key, chosen_hash)
print("Digest:    " + str(digest))
print("Signature: " + str(signature))

# Se verifica la firma del digest:
print("The signature is the same", end=": ")
print(verifySign_ECDSA(digest, signature, chosen_hash, public_key))

"""# **Comparing EXECUTION TIME of algorithms**

## Settings
"""

# Cantidad de veces que se va a repetir la ejecución de cada algoritmo (excepto encriptación y desencriptación con RSA):
n_repeat = 1000

# Cantidad de veces que se va a repetir la ejecución de cada algoritmo (sólo RSA encrypt y decrypt):
repeat = 10


# Retorna una cadena con el menor tiempo de ejecución de una lista:
def getMinExecutionTime(listExecutionTime):
    return str(min(listExecutionTime))


# Retorna una cadena con el mayor tiempo de ejecución de una lista:
def getMaxExecutionTime(listExecutionTime):
    return str(max(listExecutionTime))


"""##  ENCRYPTING: AES-128-CTR"""

# Se genera la clave:
key = os.urandom(32)

# Se obtienen el mejor y el peor tiempo en segundos:
list_et = []

for i in range(0, n_repeat):
    start = timer()
    ciphertext, iv = encrypt_AES_128_CTR(file, key)
    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""##  DECRYPTING: AES-128-CTR"""

# NOTA: Se necesita correr previamente la celda anterior.

# Se obtienen el mejor y el peor tiempo en segundos:
list_et = []
for i in range(0, n_repeat):
    start = timer()
    decrypt_AES_128_CTR(ciphertext, key, iv)
    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""##  ENCRYPTING: RSA"""

# Se generan las claves pública y privada:
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Se obtiene la lista con los pedazos de la cadena de bytes:
lstStr = chunk(file)

list_et = []

for i in range(0, repeat):
    lstCt = []

    start = timer()

    # Se van iterando los pedazos de cadena:
    for b_str in lstStr:
        # Se encripta:
        ciphertext = encrypt_RSA(b_str, public_key)
        lstCt.append(ciphertext)

    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""##  DECRYPTING: RSA"""

# NOTA: Se necesita correr previamente la celda anterior.

# Se obtienen el mejor y el peor tiempo en segundos:
list_et = []
for i in range(0, repeat):
    start = timer()

    d_message = []
    message = b""

    # Se van iterando los pedazos de cadena:
    for ciphertext in lstCt:
        # Se desencripta:
        d_message.append(decrypt_RSA(ciphertext, private_key))
    message = b"".join(d_message)

    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""## SIGNING a message: RSA"""

# Se generan las claves pública y privada para RSA:
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Se genera la clave para AES-128-CTR:
key = os.urandom(32)
# Se encripta el mensaje con AES-128-CTR:
ciphertext, iv = encrypt_AES_128_CTR(file, key)

# Se selecciona el tipo de hash:
chosen_hash = hashes.SHA256()

# Se obtienen el mejor y el peor tiempo en segundos:
list_et = []
for i in range(0, n_repeat):
    start = timer()
    # Se firma el digest:
    signature = signText_RSA(ciphertext, chosen_hash, private_key)
    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""## VERIFYING a signature of a message: RSA"""

# NOTA: Se necesita correr previamente la celda anterior.
list_et = []

for i in range(0, n_repeat):
    start = timer()
    # Se firma el digest:
    verifySign_RSA(ciphertext, signature, chosen_hash, public_key)
    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""## SIGNING a message: ECDSA"""

# Se crean las claves privada y pública:
private_key = ec.generate_private_key(ec.SECP384R1())
public_key = private_key.public_key()

# Se genera la clave para AES-128-CTR:
key = os.urandom(32)
# Se encripta el mensaje con AES-128-CTR:
ciphertext, iv = encrypt_AES_128_CTR(file, key)

# Se selecciona el tipo de hash:
chosen_hash = hashes.SHA256()

# Se obtienen el mejor y el peor tiempo en segundos:
list_et = []
for i in range(0, n_repeat):
    start = timer()
    # Se firma el digest:
    signature = signText_ECDSA(ciphertext, private_key, chosen_hash)
    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")

"""## VERIFYING a signature of a message: ECDSA"""

# NOTA: Se necesita correr previamente la celda anterior.

# Se obtienen el mejor y el peor tiempo en segundos:
list_et = []
for i in range(0, n_repeat):
    start = timer()
    # Se firma el digest:
    verifySign_ECDSA(ciphertext, signature, chosen_hash, public_key)
    end = timer()
    list_et.append(end - start)

print("Best ET:  " + getMinExecutionTime(list_et) + " seconds")
print("Worst ET: " + getMaxExecutionTime(list_et) + " seconds")
