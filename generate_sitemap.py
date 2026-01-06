#!/usr/bin/env python3
"""
Script para generar sitemap.xml automáticamente
Escanea todas las páginas HTML y las añade al sitemap con prioridades optimizadas

Uso:
    python generate_sitemap.py

El script:
1. Escanea todos los archivos .html en la raíz y carpeta publicaciones/
2. Extrae metadata de los archivos (fecha de modificación)
3. Genera sitemap.xml con prioridades SEO optimizadas
4. Incluye páginas estáticas y legales

Autor: Hathor Ascend
Fecha: 2026-01-06
"""

import os
import glob
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Configuración
BASE_URL = "https://www.hathorascend.com"
OUTPUT_FILE = "sitemap.xml"

# Definir páginas estáticas con metadatos
STATIC_PAGES = [
    {
        "url": "/",
        "priority": "1.0",
        "changefreq": "daily",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "url": "/acerca.html",
        "priority": "0.9",
        "changefreq": "monthly",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "url": "/coaching-estrategico.html",
        "priority": "0.9",
        "changefreq": "weekly",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "url": "/publicaciones.html",
        "priority": "0.8",
        "changefreq": "daily",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "url": "/aviso-legal",
        "priority": "0.3",
        "changefreq": "yearly",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "url": "/politicas.html",
        "priority": "0.3",
        "changefreq": "yearly",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "url": "/.well-known/security.txt",
        "priority": "0.1",
        "changefreq": "yearly",
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    }
]

def get_file_modification_date(filepath):
    """Obtiene la fecha de modificación de un archivo"""
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except:
        return datetime.now().strftime("%Y-%m-%d")

def find_blog_posts():
    """Encuentra todos los artículos del blog en la carpeta publicaciones/"""
    posts = []
    
    # Buscar archivos HTML en publicaciones/
    pattern = "publicaciones/*.html"
    for filepath in glob.glob(pattern):
        filename = os.path.basename(filepath)
        url = f"/publicaciones/{filename}"
        lastmod = get_file_modification_date(filepath)
        
        posts.append({
            "url": url,
            "priority": "0.7",
            "changefreq": "monthly",
            "lastmod": lastmod
        })
    
    return posts

def generate_sitemap(pages):
    """Genera el XML del sitemap"""
    # Crear elemento raíz
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Añadir cada página
    for page in pages:
        url = SubElement(urlset, 'url')
        
        loc = SubElement(url, 'loc')
        loc.text = BASE_URL + page['url']
        
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = page['lastmod']
        
        changefreq = SubElement(url, 'changefreq')
        changefreq.text = page['changefreq']
        
        priority = SubElement(url, 'priority')
        priority.text = page['priority']
    
    return urlset

def prettify_xml(elem):
    """Formatea el XML para que sea legible"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8")

def main():
    print("\n🚀 Generando sitemap.xml...\n")
    
    # Recopilar todas las páginas
    all_pages = STATIC_PAGES.copy()
    
    # Añadir artículos del blog
    blog_posts = find_blog_posts()
    all_pages.extend(blog_posts)
    
    print(f"✅ Páginas estáticas encontradas: {len(STATIC_PAGES)}")
    print(f"✅ Artículos del blog encontrados: {len(blog_posts)}")
    print(f"📊 Total de URLs: {len(all_pages)}\n")
    
    # Generar sitemap
    sitemap = generate_sitemap(all_pages)
    
    # Guardar archivo
    xml_string = prettify_xml(sitemap)
    
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(xml_string)
    
    print(f"✅ Sitemap generado exitosamente: {OUTPUT_FILE}")
    print(f"🌐 URL: {BASE_URL}/sitemap.xml\n")
    
    # Mostrar resumen de URLs
    print("📝 URLs incluidas:")
    for page in all_pages:
        print(f"  • {BASE_URL}{page['url']} (prioridad: {page['priority']})")
    
    print("\n🚀 ¡Listo! Ahora puedes hacer commit y push a GitHub.")
    print("🔄 El sitemap se actualizará automáticamente en Google Search Console.\n")

if __name__ == "__main__":
    main()
