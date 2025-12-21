import re

archivos = ['publicaciones.html', 'articulo1.html', 'articulo2.html', 'articulo03.html']

for archivo in archivos:
    print(f"Procesando {archivo}...")
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Reemplazar bloque <style>...</style> con link externo
        contenido_nuevo = re.sub(
            r'<style>.*?</style>',
            '<link rel="stylesheet" href="styles.css">',
            contenido,
            flags=re.DOTALL
        )
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print(f"  ✓ {archivo} actualizado correctamente")
    except Exception as e:
        print(f"  ✗ Error en {archivo}: {e}")

print("\n¡Completado! Ahora ejecuta:")
print("  git add .")
print('  git commit -m "Migrar CSS inline a archivo externo (styles.css)"')
print("  git push origin main")
