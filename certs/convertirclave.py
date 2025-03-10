import os
import subprocess
import getpass  # Para pedir la contraseña sin mostrarla en pantalla

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta actual (certs/)
CSD_KEY_DER = os.path.join(BASE_DIR, "CSD.key")  # Archivo original en formato DER
CSD_KEY_PEM = os.path.join(BASE_DIR, "CSD_pem.key")  # Archivo convertido a PEM

# Pedir la contraseña de forma segura
CSD_PASSWORD = getpass.getpass(" Ingresa la contraseña del CSD: ")

# Ruta absoluta de OpenSSL en Windows
OPENSSL_PATH = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"

# Comando para convertir la clave de DER a PEM
openssl_command = [
    OPENSSL_PATH, "pkcs8", "-inform", "DER",
    "-in", CSD_KEY_DER,
    "-out", CSD_KEY_PEM,
    "-passin", f"pass:{CSD_PASSWORD}"
]

try:
    # Ejecutar OpenSSL directamente desde su ruta absoluta
    result = subprocess.run(openssl_command, capture_output=True, text=True, check=True)

    if result.returncode == 0:
        print(f" La clave privada ha sido convertida correctamente a PEM: {CSD_KEY_PEM}")
    else:
        print(f"Error en OpenSSL: {result.stderr}")

except FileNotFoundError:
    print("Error: OpenSSL no está instalado o la ruta no es correcta.")
    print("🔹 Revisa la ruta en OPENSSL_PATH y vuelve a intentarlo.")
except subprocess.CalledProcessError as e:
    print(f"Error al convertir la clave privada: {e.stderr}")
