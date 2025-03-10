import os
import base64
import xml.etree.ElementTree as ET
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# 📌 Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Directorio raíz
CSD_CER = os.path.join(BASE_DIR, "certs", "CSD.cer")  # Certificado en formato .cer
CSD_KEY = os.path.join(BASE_DIR, "certs", "CSD_pem.key")  # Clave privada convertida a PEM
XML_PATH = os.path.join(BASE_DIR, "xml", "cfdi.xml")  # XML original
SIGNED_XML_PATH = os.path.join(BASE_DIR, "xml", "cfdi_firmado.xml")  # XML firmado

# 📌 Pedir la contraseña para desencriptar la clave privada
CSD_PASSWORD = b"?????"   

# 📌 Verificar que los archivos existen antes de continuar
for file_path in [CSD_CER, CSD_KEY, XML_PATH]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f" Error: No se encontró el archivo {file_path}")

# 📌 Leer el XML CFDI
tree = ET.parse(XML_PATH)
root = tree.getroot()

# 📌 Generar la cadena original del CFDI (Ejemplo simplificado, debe seguir el estándar del SAT)
cadena_original = "||" + root.attrib["Version"] + "|" + root.attrib["Serie"] + "|" + root.attrib["Folio"] + "||"

# 📌 Leer la llave privada en formato PEM y cargarla con la contraseña
with open(CSD_KEY, "rb") as key_file:
    key_data = key_file.read()

private_key = load_pem_private_key(key_data, password=None)

# 📌 Firmar la cadena original con SHA256 usando Cryptography
firma = private_key.sign(
    cadena_original.encode("utf-8"),
    padding.PKCS1v15(),
    hashes.SHA256()
)

# 📌 Convertir la firma a Base64
sello_digital = base64.b64encode(firma).decode()

# 📌 Insertar el sello en el XML
root.set("Sello", sello_digital)

# 📌 Guardar el XML firmado
tree.write(SIGNED_XML_PATH, encoding="utf-8", xml_declaration=True)

print(f" XML firmado correctamente: {SIGNED_XML_PATH}")

