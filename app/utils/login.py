import uuid

# Cadena hexadecimal de SQL
hex_string_from_sql = "33336d2c-b03f-11ee-a210-0a0027000003"
"""
46983916
33336d2c-b03f-11ee-a210-0a0027000003
"""
# Eliminar guiones y convertir a un formato adecuado
hex_string = hex_string_from_sql.replace("-", "")
hex_bytes = bytes.fromhex(hex_string)

# Imprimir el resultado
print(hex_bytes)
import uuid

# Cadena hexadecimal de SQL
hex_string_from_sql = "33336d2c-b03f-11ee-a210-0a0027000003"

# Eliminar guiones y convertir a un formato adecuado
hex_string = hex_string_from_sql.replace("-", "")
hex_bytes = bytes.fromhex(hex_string)

# Convertir bytes a un entero
integer_value = int.from_bytes(hex_bytes, byteorder='big')

# Imprimir el resultado
print(integer_value)
