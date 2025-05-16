import re
from pathlib import Path
import os

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
        lambda m: f'<link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'{m.group(1).lstrip("/static/")[3:]}\') }}}}">',
        content
    )

    # Заменяем ссылки на JS
    content = re.sub(
        patterns['src'],
        lambda m: f'<script src="{{{{ url_for(\'static\', filename=\'{m.group(1).lstrip("/static/")[3:]}\') }}}}"></script>',
        content
    )

    # Заменяем ссылки на изображения
    content = re.sub(
        patterns['img'],
        lambda m: f'<img src="{{{{ url_for(\'static\', filename=\'{m.group(1).lstrip("/static/")[3:]}\') }}}}">',
        content
    )

    # Заменяем другие статические ссылки (например, в атрибутах)
    content = re.sub(
        patterns['static'],
        lambda m: f'{{{{ url_for(\'static\', filename=\'{m.group(1).lstrip("/static/")[3:]}\') }}}}',
        content
    )
 
    # Записываем измененное содержимое в оригинальный файл
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(content)


