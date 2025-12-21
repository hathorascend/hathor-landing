# hathor-landing

Landing page para Hathor Ascend - Coaching de transformación personal

## 📝 Sistema de Publicaciones en Markdown

Este repositorio incluye un sistema completo para crear publicaciones de blog en formato Markdown y convertirlas automáticamente a HTML con el estilo de Hathor Ascend.

### 📦 Estructura del Proyecto

```
hathor-landing/
├── posts_md/              # Publicaciones en Markdown
│   └── plantilla-post.md  # Plantilla para nuevas publicaciones
├── md_to_html.py         # Script de conversión MD → HTML
├── update_posts.py       # Script para actualizar publicaciones.html
├── publicaciones.html    # Página índice de publicaciones
├── *.html                # Archivos HTML de publicaciones
└── styles.css            # Estilos del sitio
```

---

## ✨ Cómo Crear una Nueva Publicación

### 1️⃣ Crear archivo Markdown

```bash
cp posts_md/plantilla-post.md posts_md/mi-nueva-publicacion.md
```

### 2️⃣ Editar frontmatter y contenido

Abre el archivo y completa los metadatos:

```markdown
---
title: "El título de tu publicación"
date: 2025-12-21
author: "Moisés Aponte"
category: "Transformación Personal"
tags: ["identidad", "acción", "hábitos"]
excerpt: "Resumen breve que aparece en la página de publicaciones (máximo 150 caracteres)"
image: "imagenes/nombre-imagen.jpg"
---

# Tu Contenido Aquí

Escribe tu artículo en Markdown...
```

### 3️⃣ Convertir a HTML

```bash
python md_to_html.py posts_md/mi-nueva-publicacion.md
```

Esto generará `mi-nueva-publicacion.html` con el estilo completo de Hathor Ascend.

### 4️⃣ Actualizar índice de publicaciones (Opcional)

```bash
python update_posts.py
```

Este script escanea automáticamente todos los archivos `.md` en `posts_md/` y actualiza `publicaciones.html`.

### 5️⃣ Subir a GitHub

```bash
git add posts_md/mi-nueva-publicacion.md
git add mi-nueva-publicacion.html
git add publicaciones.html
git commit -m "Add new post: [título]"
git push origin main
```

---

## 🎨 Sintaxis Markdown Soportada

| Markdown | HTML Generado |
|----------|---------------|
| `# Título` | `<h1>Título</h1>` |
| `## Subtítulo` | `<h2>Subtítulo</h2>` |
| `### Subsección` | `<h3>Subsección</h3>` |
| `**negrita**` | `<strong>negrita</strong>` |
| `*cursiva*` | `<em>cursiva</em>` |
| `> Cita` | `<blockquote><p>Cita</p></blockquote>` |
| `- Lista` | `<ul><li>Lista</li></ul>` |
| `1. Numerada` | `<li>Numerada</li>` |

---

## 🛠️ Scripts Incluidos

### `md_to_html.py`

Converte archivos Markdown a HTML con la estructura completa de Hathor Ascend.

**Uso:**
```bash
python md_to_html.py posts_md/archivo.md
```

**Funciones:**
- Extrae frontmatter YAML
- Convierte Markdown a HTML
- Genera página completa con header, footer y estilos
- Incluye metadatos (título, fecha, categoría)

### `update_posts.py`

Actualiza automáticamente el índice de publicaciones.

**Uso:**
```bash
python update_posts.py
```

**Funciones:**
- Escanea carpeta `posts_md/`
- Extrae frontmatter de cada post
- Genera tarjetas HTML ordenadas por fecha
- Actualiza `publicaciones.html`

---

## 📚 Ejemplo de Publicación

**Archivo:** `posts_md/la-brecha-identidad.md`

```markdown
---
title: "La brecha entre quién eres y quién quieres ser"
date: 2025-12-21
author: "Moisés Aponte"
category: "Identidad"
tags: ["transformación", "identidad", "acción"]
excerpt: "El problema no es que no sepas qué hacer. El problema es la versión de ti mismo que sostienes día tras día."
image: "imagenes/brecha.jpg"
---

# La brecha entre quién eres y quién quieres ser

## El problema no es externo

**La mayoría de las personas están convencidas de que su valor está en lo que sueñan.**

Pero tu valor no está en tus sueños. Está en tu agenda.

> Si repites excusas, eres alguien que se organiza alrededor de la excusa.

No es problemático que no sepas qué hacer. Es problemático **repetir la versión de ti** que te mantiene atascado.

## La identidad es acción

Tus sueños pueden decir que eres alguien ambicioso. Tus hábitos pueden decir que no.

**Y entre lo que imaginas y lo que repites, siempre gana lo que repites.**
```

**Comando:**
```bash
python md_to_html.py posts_md/la-brecha-identidad.md
```

**Resultado:** `la-brecha-identidad.html` con estructura completa

---

## ✅ Checklist para cada Publicación

- [ ] Crear archivo `.md` en `posts_md/`
- [ ] Completar frontmatter (título, fecha, categoría, excerpt)
- [ ] Escribir contenido en Markdown
- [ ] Ejecutar `python md_to_html.py posts_md/nombre.md`
- [ ] Revisar HTML generado
- [ ] Ejecutar `python update_posts.py` (opcional)
- [ ] Commit y push a GitHub
- [ ] Verificar en hathorascend.com

---

## 📌 Notas Importantes

1. **No edites los archivos HTML directamente** - siempre trabaja desde los archivos `.md`
2. **Usa nombres descriptivos** para tus archivos (ej: `la-brecha-identidad.md`)
3. **Fecha en formato ISO** - usa `YYYY-MM-DD` (ej: `2025-12-21`)
4. **Excerpt breve** - máximo 150 caracteres para visualización correcta
5. **Tags relevantes** - ayudan a organizar el contenido

---

## 🚀 Deployment

El sitio se despliega automáticamente en GitHub Pages cuando haces push a `main`.

**URL:** [https://www.hathorascend.com](https://www.hathorascend.com)

---

## 👤 Autor

**Moisés Aponte**
- Coach de Transformación Personal
- Hathor Ascend - Disciplina · Claridad · Estructura

---

## 📝 Licencia

© 2025 Hathor Ascend. Todos los derechos reservados.
