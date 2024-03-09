import os, sys, random, time, subprocess, platform, ctypes
from icecream import ic

VALID_EXTENSIONS = [
    "apng",
    "avif",
    "gif",
    "jpg",
    "jpeg",
    "jfif",
    "pjpeg",
    "pjp",
    "png",
    "svg",
    "webp",
    "bmp",
    "ico",
    "cur",
    "tif",
    "tiff",
]


def run(folder_path, interval):
    img_paths = get_random_img_paths(folder_path)
    img_names = [os.path.basename(img_path) for img_path in img_paths]
    ic(img_names)
    while True:
        for img_path in img_paths:
            set_wallpaper(img_path)
            time.sleep(interval)


def get_random_img_paths(folder_path):
    file_names = os.listdir(folder_path)
    img_names = [file_name for file_name in file_names if is_valid_extension(file_name)]
    img_paths = [os.path.join(folder_path, img_name) for img_name in img_names]
    random.shuffle(img_paths)
    return img_paths


def is_valid_extension(file_name):
    for extension in VALID_EXTENSIONS:
        if file_name.lower().endswith("." + extension):
            return True
    return False


def set_wallpaper(img_path):
    system = platform.system()
    if system == "Linux":
        set_wallpaper_linux(img_path)
    elif system == "Windows":  # not tested
        set_wallpaper_windows(img_path)
    else:
        print(f"error: operating system {system} is not supported")


def set_wallpaper_linux(img_path):
    command = ""
    desktop_env = os.environ.get("DESKTOP_SESSION")

    if desktop_env == "ubuntu":
        command = get_ubuntu_command(img_path)
    elif desktop_env == "gnome":  # not tested
        command = (
            f"gsettings set org.gnome.desktop.background picture-uri file://{img_path}"
        )
    elif desktop_env == "kde":  # not tested
        command = f'qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript \'var allDesktops = desktops();for (i=0;i<allDesktops.length;i++) {{d = allDesktops[i]; d.wallpaperPlugin = "org.kde.image"; d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General"); d.writeConfig("Image", "file://{img_path}")}}\''
    elif desktop_env == "xfce":  # not tested
        command = f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s {img_path}"
    elif desktop_env == "unity":  # not tested
        command = (
            f"gsettings set org.gnome.desktop.background picture-uri file://{img_path}"
        )
    elif desktop_env == "cinnamon":  # not tested
        command = f"gsettings set org.cinnamon.desktop.background picture-uri file://{img_path}"
    else:
        print(f"error: desktop environment {desktop_env} is not supported")

    if command:
        os.system(command)
        print(f"wallpaper changed to {os.path.basename(img_path)}")
    else:
        print(f"error: could not set wallpaper {os.path.basename(img_path)}")


def get_ubuntu_command(img_path):
    # command is different if color-scheme is dark
    color_scheme = get_system_color_scheme()
    if not color_scheme:
        print("error: color-scheme for ubuntu environment not found")
    elif "dark" in color_scheme:
        return f"gsettings set org.gnome.desktop.background picture-uri-dark file://{img_path}"
    else:
        return (
            f"gsettings set org.gnome.desktop.background picture-uri file://{img_path}"
        )


def get_system_color_scheme():
    try:
        output = (
            subprocess.check_output(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"]
            )
            .decode()
            .strip()
        )
        return output
    except subprocess.CalledProcessError:
        return


def set_wallpaper_windows(img_path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 3)
        print(f"Wallpaper changed to {os.path.basename(img_path)}")
    except Exception as e:
        print(f"error: could not set wallpaper {os.path.basename(img_path)}")


if __name__ == "__main__":
    # python3 {folder_path} {interval}
    if len(sys.argv) < 2:
        print("error: you must provide a folder_path")
        exit()
    folder_path = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) >= 3 else 60
    run(folder_path, interval)
