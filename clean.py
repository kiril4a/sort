import os
import shutil
from transliterate import translit
from sys import argv
import patoolib

def normalize(filename):
    # Транслітерація та видалення заборонених символів
    trans_filename = translit(filename, 'ru', reversed=True)
    return ''.join(c if c.isalnum() or c in {'_', '.'} else '_' for c in trans_filename)


def process_folder(folder_path):
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            process_file(item_path)
        elif os.path.isdir(item_path):
            process_folder(item_path)

    # Видаляємо порожні папки
    if not os.listdir(folder_path):
        os.rmdir(folder_path)


def extract_archive(file_path):
    # Отримати ім'я архіву без розширення
    archive_name = os.path.splitext(os.path.basename(file_path))[0]

    # Створити папку для розархівації
    extract_path = os.path.join(os.path.dirname(file_path), archive_name)
    os.makedirs(extract_path, exist_ok=True)

    # Розархівація архіву з використанням patoolib
    patoolib.extract_archive(file_path, outdir=extract_path)


def process_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.upper()[1:]

    category = get_category(file_extension)

    # Створюємо відповідну папку, якщо її ще немає
    category_folder = os.path.join(folder_path, category)
    os.makedirs(category_folder, exist_ok=True)
    # Нормалізуємо ім'я файлу та перейменовуємо
    new_filename = normalize(os.path.basename(file_path))
    new_filepath = os.path.join(category_folder, new_filename)

    shutil.move(file_path, new_filepath)
    if category == 'archives':
        extract_archive(new_filepath)
        os.remove(new_filepath)


def get_category(file_extension):
    image_extensions = {'JPEG', 'PNG', 'JPG', 'SVG'}
    video_extensions = {'AVI', 'MP4', 'MOV', 'MKV'}
    document_extensions = {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'}
    music_extensions = {'MP3', 'OGG', 'WAV', 'AMR'}
    archive_extensions = {'ZIP', 'GZ', 'TAR'}

    if file_extension in image_extensions:
        return 'images'
    elif file_extension in video_extensions:
        return 'videos'
    elif file_extension in document_extensions:
        return 'documents'
    elif file_extension in music_extensions:
        return 'audio'
    elif file_extension in archive_extensions:
        return 'archives'
    else:
        return 'other'


def main():
    global folder_path
    if len(argv) != 2:
        print("Usage: python sort.py <folder_path>")
        exit(1)
    folder_path = argv[1]

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("Invalid folder path.")
        exit(1)

    process_folder(folder_path)
    print("Sorting completed.\n")

    categories = ['images', 'videos', 'documents', 'audio', 'archives', 'other']
    print("\nList of files in each category:\n")
    for category in categories:
        category_folder = os.path.join(folder_path, category)
        if os.path.exists(category_folder):
            category_files = os.listdir(category_folder)
            print(f"\n{category}: {category_files}")
        else:
            print(f"\n{category}: No files")

    print("\nList of known script extensions:\n")
    known_extensions = {'JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
                        'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR',
                        'ZIP', 'GZ', 'TAR'}
    print(known_extensions)

    print("\nList of unknown extensions:\n")
    all_files = os.listdir(folder_path)
    unknown_extensions = {os.path.splitext(file)[1].upper()[1:] for file in all_files if
                          os.path.isfile(os.path.join(folder_path, file))}
    unknown_extensions -= known_extensions
    if len(unknown_extensions) == 0:
        print("None")
    else:
        print(unknown_extensions)

    if __name__ == "__main__":
        main()