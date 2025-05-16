import os, shutil
from tqdm import tqdm
from pathlib import Path
from replace_link import replace_static_links

def find_html_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.html'):
                full_path = Path(root) / file
                html_files.append(str(full_path))
    return html_files


def recursive_copy(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        source_item = os.path.join(src, item)
        dest_item = os.path.join(dst, item)
        if os.path.isdir(source_item):
            recursive_copy(source_item, dest_item)
        else:
            shutil.copy2(source_item, dest_item)


if __name__ == "__main__":
    print("Программа для замены в html файлаx статических ссылок на ссылки вида url_for")
    print("Пример пути: C:\work\\benua.hsitmo.ru\BenuaAddresses-Frontend-main\html")
    search_dir = input("Путь до папки: ")
    print(search_dir)
    
    if not os.path.exists(search_dir):
        print(f"Директория {search_dir} не существует!")
        exit(1)
    
    print(f"Поиск HTML-файлов в {search_dir}...")
    html_files = find_html_files(search_dir)

    # О найденом
    if not html_files:
        print("HTML-файлы не найдены.")
    else:
        print(f"Найдено {len(html_files)} HTML-файлов:")
        for i, file in enumerate(html_files, 1):
            print(f"{i}. {file}")
    
    # бэкап
    backups_path =  search_dir + "_backups"
    
    if os.path.exists(backups_path):
        print(f"Папка `{backups_path}` уже существует! Новых бекапов не будет!")
        
    else:
        recursive_copy(search_dir, backups_path)
        
    

            
    for html_file in tqdm(html_files):
        replace_static_links(html_file)

    print("Готово!")
