from werkzeug.security import generate_password_hash

# Escribe aquí la contraseña que quieras usar
mi_clave = "admin123456" 

# Generamos el hash (el código cifrado)
clave_cifrada = generate_password_hash(mi_clave)

print("\n" + "="*50)
print(f"CONTRASEÑA ORIGINAL: {mi_clave}")
print("-" * 50)
print(f"COPIA ESTE HASH PARA TU BASE DE DATOS:\n\n{clave_cifrada}")
print("="*50 + "\n")