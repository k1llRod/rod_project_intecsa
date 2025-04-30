import csv
import sys
from xmlrpc import client

# ————— CONFIGURA ESTO —————
url      = "http://localhost:8070"
db       = "intecsa"
username = "admin"
password = "admin"
csv_file = "imagenes.csv"  # tu CSV con default_code,base64_image
# ———————————————————————
try:
    csv.field_size_limit(sys.maxsize)
except OverflowError:
    csv.field_size_limit(2**31 - 1)
# Conexión
common = client.ServerProxy(f"{url}/xmlrpc/2/common")
uid    = common.authenticate(db, username, password, {})
models = client.ServerProxy(f"{url}/xmlrpc/2/object")

# Leer CSV y actualizar
# Leer CSV e importar imágenes
with open(csv_file, newline='', encoding='utf-8-sig') as f:
    # Leemos la primera línea para los encabezados
    reader = csv.reader(f, delimiter=',', quotechar='"')
    raw_headers = next(reader)
    # Limpiamos espacios y comillas
    headers = [h.strip().strip('"').lower() for h in raw_headers]
    # Re-creamos el DictReader con los headers limpios
    dict_reader = csv.DictReader(f, fieldnames=headers, delimiter=',', quotechar='"')
    for row in reader:
        default_code_raw = row[0]
        default_code = default_code_raw.strip() if default_code_raw else ''

        image_raw = row[1]
        image_b64 = image_raw.strip() if image_raw else ''

        if not default_code or not image_b64:
            print("⏭ Fila saltada por falta de datos:", row)
            continue

        # Buscar plantilla por default_code
        tmpl_ids = models.execute_kw(db, uid, password,
            'product.template', 'search',
            [[['default_code','=', default_code]]])

        if not tmpl_ids:
            print(f"❌ No encontrado: {default_code}")
            continue

        # Actualizar image_1920
        models.execute_kw(db, uid, password,
            'product.template', 'write',
            [tmpl_ids, {'image_1920': image_b64}])
        print(f"✔ Imagen importada para {default_code}")