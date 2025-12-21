import sys
import os
import re
from datetime import datetime


def parse_frontmatter(md_content):
    """Extrae el frontmatter y el contenido del archivo Markdown."""
    if not md_content.startswith('---'):
        return {}, md_content

    parts = md_content.split('---', 2)
    if len(parts) < 3:
        return {}, md_content

    frontmatter_text = parts[1].strip()
    frontmatter = {}

    for line in frontmatter_text.split('\n'):
        if ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip('[]').replace('"', '').replace("'", '').strip()

        if ',' in value:
            frontmatter[key] = [t.strip() for t in value.split(',') if t.strip()]
        else:
            frontmatter[key] = value

    content = parts[2].strip()
    return frontmatter, content


def markdown_to_html(md_content):
    """Convierte Markdown a HTML básico."""
    html = md_content

    # Encabezados (mantenemos solo ## y ###, el H1 va en el template)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    # H1 manual si empiezas línea con "** "
    html = re.sub(r'^\*\* (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Énfasis
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Bloques de cita
    lines = html.split('\n')
    in_blockquote = False
    result_lines = []

    for line in lines:
        if line.startswith('> '):
            if not in_blockquote:
                result_lines.append('<blockquote>')
                in_blockquote = True
            result_lines.append('<p>' + line[2:].strip() + '</p>')
        else:
            if in_blockquote:
                result_lines.append('</blockquote>')
                in_blockquote = False
            result_lines.append(line)

    if in_blockquote:
        result_lines.append('</blockquote>')

    html = '\n'.join(result_lines)

    # Listas ordenadas simples (1. Item)
    lines = html.split('\n')
    list_processed = []
    in_ol = False

    for line in lines:
        match = re.match(r'^(\d+)\.\s+(.*)', line)
        if match:
            if not in_ol:
                list_processed.append('<ol>')
                in_ol = True
            list_processed.append(f'<li>{match.group(2)}</li>')
        else:
            if in_ol:
                list_processed.append('</ol>')
                in_ol = False
            list_processed.append(line)

    if in_ol:
        list_processed.append('</ol>')

    html = '\n'.join(list_processed)

    # Párrafos
    paragraphs = []
    for para in html.split('\n\n'):
        para = para.strip()
        if not para:
            continue
        if para.startswith('<'):
            paragraphs.append(para)
        else:
            paragraphs.append(f'<p>{para}</p>')

    return '\n\n'.join(paragraphs)


def create_html_page(frontmatter, content_html, output_filename):
    title = frontmatter.get('title', 'Sin título')
    date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    author = frontmatter.get('author', 'Moisés Aponte')
    category = frontmatter.get('category', 'Transformación Personal')

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} - Hathor Ascend</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
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
                <a href="../index.html">Inicio</a>
                <a href="index.html#sistema">Sistema</a>
                <a href="index.html#para-quien">Para quién</a>
                <a href="../publicaciones.html">Publicaciones</a>
            </nav>
        </div>
    </header>
    <main>
        <div class="page">
            <a href="../publicaciones.html" class="back-link">← Volver a publicaciones</a>
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
</html>"""

    # Asegura que el directorio exista
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

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
    output_file = f"publicaciones/{base_name}.html"

    frontmatter = create_html_page(frontmatter, content_html, output_file)

    print(f"✅ Archivo generado: {output_file}")
    print(f"📝 Título: {frontmatter.get('title', 'Sin título')}")
    print(f"📅 Fecha: {frontmatter.get('date', 'No especificada')}")
    print("\n⚠️ RECUERDA:")
    print("   Añade esta publicación a publicaciones.html manualmente")
    print("   o ejecuta: python update_posts.py")


if __name__ == "__main__":
    main()
