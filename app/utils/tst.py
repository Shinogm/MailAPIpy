import bcrypt

# Contraseña proporcionada por el usuario
contrasena_usuario = "ola"

# Hash almacenado en la base de datos
hash_almacenado = '$2b$12$OiJZfu9lO6zB9TBoUmiMyePslJU.fIjYNXIhLstquCTEACoVtNFsu'

# Verificar la contraseña
if bcrypt.checkpw(contrasena_usuario.encode('utf-8'), hash_almacenado.encode('utf-8')):
    print("Inicio de sesión exitoso")
else:
    print("La contraseña es incorrecta")
