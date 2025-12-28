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
    # Normaliza saltos de línea múltiples
    html = re.sub(r'\n{3,}', '\n\n', html)

    for para in html.split('\n\n'):
        para = para.strip()
        if not para:
            continue

        # Si el bloque ya es HTML de bloque, no lo envuelvas
        if para.startswith('<h') or para.startswith('<ol') or para.startswith('<ul') \
           or para.startswith('<li') or para.startswith('<blockquote') \
           or para.startswith('</blockquote') or para.startswith('<p'):
            paragraphs.append(para)
        else:
            paragraphs.append(f'<p>{para}</p>')

    return '\n\n'.join(paragraphs)

    


def create_html_page(frontmatter, content_html, output_filename, base_name):

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

                
            <!-- Botones para compartir -->
            <div class="share-buttons">
                <p class="share-label">Compartir este artículo:</p>
                <div class="share-icons">
                    <a href="https://wa.me/?text={title}%20-%20https://hathorascend.com/publicaciones/{base_name}.html" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       class="share-btn whatsapp"
                       aria-label="Compartir en WhatsApp">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                        </svg>
                        WhatsApp
                    </a>
                    <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://hathorascend.com/publicaciones/{base_name}.html" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       class="share-btn linkedin"
                       aria-label="Compartir en LinkedIn">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                        LinkedIn
                    </a>
                    <a href="https://www.facebook.com/sharer/sharer.php?u=https://hathorascend.com/publicaciones/{base_name}.html" 
                       target="_blank" 
                       rel="noopener noreferrer" 
                       class="share-btn facebook"
                       aria-label="Compartir en Facebook">
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                        Facebook
                    </a>
                </div>
            </div>
            
            </article>
                    <!-- Bloque CTA coaching estratégico -->
        <section class="ha-cta-coaching">
          <p>
            Si este artículo describe más de lo que te gustaría admitir
            y quieres trabajar esto con estructura, no con buenas intenciones,
            puedes solicitar un proceso de coaching estratégico 1:1 conmigo.
          </p>
          <p>
            <a href="/coaching-estrategico.html">
              Ver cómo funciona el proceso de coaching estratégico Hathor →
            </a>
          </p>
        </section>
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

    frontmatter = create_html_page(frontmatter, content_html, output_file, base_name)
    print(f"✅ Archivo generado: {output_file}")
    print(f"📝 Título: {frontmatter.get('title', 'Sin título')}")
    print(f"📅 Fecha: {frontmatter.get('date', 'No especificada, base_name')}")
    print("\n⚠️ RECUERDA:")
    print("   Añade esta publicación a publicaciones.html manualmente")
    print("   o ejecuta: python update_posts.py")


if __name__ == "__main__":
    main()
