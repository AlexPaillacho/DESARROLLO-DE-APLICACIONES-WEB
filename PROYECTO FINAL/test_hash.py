from werkzeug.security import generate_password_hash

# Para cada usuario que creemos debemos hacer un hash de la contraseña
# Colocamos la contraseña y guardamos y ejecutamos el siguiente comando
#     python test_hash.py 
   
mi_clave = "admin123456" 

# Generamos el hash (el código cifrado)
clave_cifrada = generate_password_hash(mi_clave)

print("\n" + "="*50)
print(f"CONTRASEÑA ORIGINAL: {mi_clave}")
print("-" * 50)
print(f"COPIA ESTE HASH PARA TU BASE DE DATOS:\n\n{clave_cifrada}")
print("="*50 + "\n")



# Al ejecutar el comando nos da un codigo copiamos el codigo en 
# nuestra base de datos en password