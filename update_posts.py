#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualiza automáticamente publicaciones.html con nuevos posts
"""
import os
import re
from datetime import datetime

def scan_posts():
    """Escanea todos los archivos .md en posts_md/"""
    posts = []
    
    if not os.path.exists('posts_md'):
        print("⚠️ No existe la carpeta posts_md/")
        return posts
    
    for filename in os.listdir('posts_md'):
        if filename.endswith('.md') and filename != 'plantilla-post.md':
            filepath = os.path.join('posts_md', filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = {}
                    for line in parts[1].strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"').strip("'")
                    
                    posts.append({
                        'filename': f"publicaciones/{filename.replace('.md', '.html')}",
                        'title': frontmatter.get('title', 'Sin título'),
                        'date': frontmatter.get('date', ''),
                        'category': frontmatter.get('category', 'General'),
                        'excerpt': frontmatter.get('excerpt', ''),
                    })
    
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def format_date(date_str):
    """Convierte 2025-12-21 a '21 de diciembre, 2025'"""
    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{date.day} de {months[date.month-1]}, {date.year}"
    except:
        return date_str

def generate_post_cards(posts):
    """Genera el HTML para las tarjetas de posts"""
    cards_html = ""
    
    for post in posts:
        date_formatted = format_date(post['date'])
        cards_html += f'''
        <div class="post-card">
            <div class="post-date">{date_formatted}</div>
            <h2 class="post-title">
                <a href="{post['filename']}">{post['title']}
                </a>
            </h2>

            <div class="post-meta">
                <span class="post-category">{post['category']}</span>
            </div>
            <p>{post['excerpt']}</p>
            <a href="{post['filename']}" class="read-more">Leer más +</a>
        </div>
        '''
    
    return cards_html

def main():
    print("🔄 Escaneando publicaciones...")
    posts = scan_posts()
    
    if not posts:
        print("❌ No se encontraron publicaciones")
        return
    
    print(f"✅ Encontradas {len(posts)} publicaciones")
    
    with open('publicaciones.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    cards_html = generate_post_cards(posts)
    
    pattern = r'(<div class="articles-grid">)(.*?)(</div>\s*</div>\s*</main>)'
    replacement = r'\1' + cards_html + r'\3'
    
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    with open('publicaciones.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ publicaciones.html actualizado")
    print("\nPublicaciones añadidas:")
    for post in posts:
        print(f"  • {post['title']}")

if __name__ == "__main__":
    main()
