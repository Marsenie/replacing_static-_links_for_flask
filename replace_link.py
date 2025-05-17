import re
from pathlib import Path
import os


def removing_dots_from_start_link(link):
    if link[:3] == "../":
        link = link[3:]
    return link


def replace_static_links(html_file_path):
    # Определяем шаблоны для поиска статических ссылок
    patterns = {
        'href': r'<link.*?href=[\'"](.*?\.css)[\'"].*?>',
        'src': r'<script.*?src=[\'"](.*?\.js)[\'"].*?>',
        'img': r'<img.*?src=[\'"](.*?\.(?:png|jpg|jpeg|gif|svg))[\'"].*?>',
        'static': r'[\'"](/static/.*?)[\'"]'
    }

    # Читаем содержимое файла
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    

    # Заменяем ссылки на CSS
    content = re.sub(
        patterns['href'],
        lambda m: f'<link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'{removing_dots_from_start_link(m.group(1).lstrip("/static/"))}\') }}}}">',
        content
    )

    # Заменяем ссылки на JS
    content = re.sub(
        patterns['src'],
        lambda m: f'<script src="{{{{ url_for(\'static\', filename=\'{removing_dots_from_start_link(m.group(1).lstrip("/static/"))}\') }}}}"></script>',
        content
    )

    # Заменяем ссылки на изображения
    content = re.sub(
        patterns['img'],
        lambda m: f'<img src="{{{{ url_for(\'static\', filename=\'{removing_dots_from_start_link(m.group(1).lstrip("/static/"))}\') }}}}">',
        content
    )

    # Заменяем другие статические ссылки (например, в атрибутах)
    content = re.sub(
        patterns['static'],
        lambda m: f'{{{{ url_for(\'static\', filename=\'{removing_dots_from_start_link(m.group(1).lstrip("/static/"))}\') }}}}',
        content
    )
 
    # Записываем измененное содержимое в оригинальный файл
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(content)


