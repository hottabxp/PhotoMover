import os
import fnmatch
import subprocess


def find_files(directory, file_patterns):
    matching_files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            for file_pattern in file_patterns:
                if fnmatch.fnmatch(filename.lower(), file_pattern.lower()):
                    matching_files.append(os.path.join(root, filename))
                    break  # файл уже найден, переходим к следующему

    return matching_files


def set_walpaper(wallpaper_path):
    # Определяем окружение рабочего стола
    desktop_environment = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

    # Устанавливаем обои рабочего стола в зависимости от окружения
    if "gnome" in desktop_environment:
        subprocess.call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{wallpaper_path}"])
    elif "kde" in desktop_environment:
        subprocess.call(["qdbus", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", f'''
            var allDesktops = desktops();
            for (i=0; i < allDesktops.length; i++) {{
                d = allDesktops[i];
                d.wallpaperPlugin = "org.kde.image";
                d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                d.writeConfig("Image", "file://{wallpaper_path}")
            }}
        '''])
    elif "xfce" in desktop_environment:
        for i in range(10):
            try:
                subprocess.call(
                    ["xfconf-query", "-c", "xfce4-desktop", "-p", f"/backdrop/screen0/monitor{i}/workspace0/last-image",
                     "-s", wallpaper_path])
            except FileNotFoundError:
                break
    else:
        print("Не удалось определить окружение рабочего стола")
