import os
import fnmatch

def find_files(directory, file_patterns):
    matching_files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            for file_pattern in file_patterns:
                if fnmatch.fnmatch(filename.lower(), file_pattern.lower()):
                    matching_files.append(os.path.join(root, filename))
                    break  # файл уже найден, переходим к следующему

    return matching_files

directory = "./"
image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]

image_files = find_files(directory, image_patterns)

for file in image_files:
    print(file)
