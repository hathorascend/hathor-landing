#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor de Markdown a HTML para publicaciones de Hathor Ascend
Uso: python md_to_html.py nombre-archivo.md
"""

import re
import sys
import os
from datetime import datetime

def parse_frontmatter(content):
    """Extrae el frontmatter YAML del markdown"""
    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_content = parts[1].strip()
            for line in fm_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    if key == 'tags' and value.startswith('['):
                        value = value.strip('[]').replace('"', '').replace("'", '')
                        frontmatter[key] = [t.strip() for t in value.split(',')]
                    else:
                        frontmatter[key] = value
            
            content = parts[2].strip()
    
    return frontmatter, content

def markdown_to_html(md_content):
    """Convierte Markdown a HTML"""
    html = md_content
    
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    lines = html.split('\n')
    in_blockquote = False
    result_lines = []
    
    for line in lines:
        if line.startswith('> '):
            if not in_blockquote:
                result_lines.append('<blockquote>')
                in_blockquote = True
            result_lines.append('<p>' + line[2:] + '</p>')
        else:
            if in_blockquote:
                result_lines.append('</blockquote>')
                in_blockquote = False
            result_lines.append(line)
    
    if in_blockquote:
        result_lines.append('</blockquote>')
    
    html = '\n'.join(result_lines)
    
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\n\g<0></ul>\n', html, flags=re.MULTILINE)
    
    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    paragraphs = []
    for para in html.split('\n\n'):
        para = para.strip()
        if para and not para.startswith('<'):
            para = '<p>' + para + '</p>'
        if para:
            paragraphs.append(para)
    
    return '\n\n'.join(paragraphs)

def create_html_page(frontmatter, content_html, output_filename):
    title = frontmatter.get('title', 'Sin título')
    date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    author = frontmatter.get('author', 'Moisés Aponte')
    category = frontmatter.get('category', 'Transformación Personal')
    
    html_template = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} - Hathor Ascend</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <div class="brand">
                <div class="brand-logo">HA</div>
                <div class="brand-text">
                    <div class="brand-name">Hathor Ascend</div>
                    <div class="brand-tagline">Disciplina · Claridad · Estructura</div>
                </div>
            </div>
            <nav class="nav" aria-label="Navegación principal">
                <a href="index.html">Inicio</a>
                <a href="index.html#sistema">Sistema</a>
                <a href="index.html#para-quien">Para quién</a>
                <a href="publicaciones.html">Publicaciones</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="page">
            <a href="publicaciones.html" class="back-link">← Volver a publicaciones</a>
            
            <article class="article-content">
                <div class="article-meta">
                    <span class="category">{category}</span>
                    <time datetime="{date}">{date}</time>
                </div>
                
                <h1>{title}</h1>
                
                {content_html}
            </article>
        </div>
    </main>

    <footer>
        <p>&copy; 2025 Hathor Ascend. Todos los derechos reservados.</p>
    </footer>
</body>
</html>'''
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return frontmatter

def main():
    if len(sys.argv) < 2:
        print("Uso: python md_to_html.py archivo.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe")
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    frontmatter, content = parse_frontmatter(md_content)
    content_html = markdown_to_html(content)
    
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}.html"
    
    frontmatter = create_html_page(frontmatter, content_html, output_file)
    
    print(f"✅ Archivo generado: {output_file}")
    print(f"📝 Título: {frontmatter.get('title', 'Sin título')}")
    print(f"📅 Fecha: {frontmatter.get('date', 'No especificada')}")
    print(f"\n⚠️  RECUERDA:")
    print(f"   Añade esta publicación a publicaciones.html manualmente")
    print(f"   o ejecuta: python update_posts.py")

if __name__ == "__main__":
    main()
