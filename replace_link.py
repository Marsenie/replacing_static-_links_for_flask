import re
from pathlib import Path
import os


def removing_dots_from_link(link):
    if link.find("../") != -1:
        link = link[:link.find("../")] + link[link.find("../")+3:]
    return link


def replace_static_links(html_file_path):
    # Шаблон
    patterns = [r'src=([\'"])(.*?)\1', r'href=([\'"])(.*?)\1']
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Функция замены
    def replacement(match):
        quote = match.group(1)  # сохраняем тип кавычек
        path = removing_dots_from_link(match.group(2))
        # Если путь уже начинается с url_for, не изменяем его
        
        answers = {
            r'src=([\'"])(.*?)\1' : f'src={quote}{{{{ url_for("static", filename="{removing_dots_from_link(path)}") }}}}{quote}',
            r'href=([\'"])(.*?)\1' : f'href={quote}{{{{ url_for("static", filename="{removing_dots_from_link(path)}") }}}}{quote}',
        }
        if (path.startswith("{{ url_for(")) or (path.startswith(('http://', 'https://', 'htpp://'))):
            return match.group(0)
        return answers[pattern]

    
    # Заменяем ссылки
    for pattern in patterns:
        content = re.sub(pattern, replacement, content)


    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

