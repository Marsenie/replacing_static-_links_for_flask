import re
from pathlib import Path
import os


def removing_dots_from_link(link):
    if link.find("../") != -1:
        link = link[:link.find("../")] + link[link.find("../")+3:]
    return link



def replace_static_links(html_file_path):
    # Шаблоны для поиска статических ссылок с исключением уже обработанных
    patterns = {
        'href': r'<link(?![^>]*url_for\([^)]*).*?href=[\'"](?!\{\{.*?\})(.*?\.css)[\'"].*?>',
        'script': r'(<script(?![^>]*url_for\([^)]*).*?src=[\'"](?!\{\{.*?\})(.*?\.js)[\'"].*?>)',
        'script_module': r'(<script(?![^>]*url_for\([^)]*).*?type=[\'"]module[\'"].*?src=[\'"](?!\{\{.*?\})(.*?\.js)[\'"].*?>)',
        'img': r'<img(?![^>]*url_for\([^)]*).*?src=[\'"](?!\{\{.*?\})(.*?\.(?:png|jpg|jpeg|gif|svg))[\'"].*?>',
        'static': r'(?<!url_for\()[\'"](?!\{\{.*?\})(/static/.*?)[\'"]'
    }

    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        

    # Заменяем ссылки на CSS (исключаем уже обработанные)
    content = re.sub(
        patterns['href'],
        lambda m: m.group(0) if 'url_for(' in m.group(0) else 
        f'<link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'{removing_dots_from_link(m.group(1).lstrip("/static/"))}\') }}}}">',
        content
    )

    # Заменяем модульные JS-скрипты (исключаем уже обработанные)
    content = re.sub(
        patterns['script_module'],
        lambda m: m.group(0) if 'url_for(' in m.group(0) else
        m.group(1).replace(
            m.group(2),
            f'{{{{ url_for(\'static\', filename=\'{removing_dots_from_link(m.group(2).lstrip("/static/"))}\') }}}}'
        ),
        content
    )
    
    # Заменяем обычные JS-скрипты (исключаем уже обработанные)
    content = re.sub(
        patterns['script'],
        lambda m: m.group(0) if 'url_for(' in m.group(0) else
        f'<script src="{{{{ url_for(\'static\', filename=\'{removing_dots_from_link(m.group(2).lstrip("/static/"))}\') }}}}"></script>',
        content
    )

    

    # Заменяем ссылки на изображения (исключаем уже обработанные)
    content = re.sub(
        patterns['img'],
        lambda m: m.group(0) if 'url_for(' in m.group(0) else
        f'<img src="{{{{ url_for(\'static\', filename=\'{removing_dots_from_link(m.group(1).lstrip("/static/"))}\') }}}}">',
        content
    )

    # Заменяем другие статические ссылки (исключаем уже обработанные)
    content = re.sub(
        patterns['static'],
        lambda m: m.group(0) if 'url_for(' in m.group(0) else
        f'{{{{ url_for(\'static\', filename=\'{removing_dots_from_link(m.group(1).lstrip("/static/"))}\') }}}}',
        content
    )

    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
