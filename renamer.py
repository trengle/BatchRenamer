import os

def batch_rename(folder, prefix="", suffix="", find_text="", replace_text="", extensions=None, dry_run=False):
    if not extensions:
        extensions = [".exr", ".jpg", ".png", ".jpeg", ".tiff", ".bmp"]

    renamed_files = []

    for filename in os.listdir(folder):
        if not any(filename.lower().endswith(ext) for ext in extensions):
            continue

        name, ext = os.path.splitext(filename)
        new_name = name

        if find_text:
            new_name = new_name.replace(find_text, replace_text or "")

        new_name = f"{prefix}{new_name}{suffix}{ext}"
        src = os.path.join(folder, filename)
        dst = os.path.join(folder, new_name)

        if src != dst:
            renamed_files.append((filename, new_name))
            if not dry_run:
                os.rename(src, dst)

    return renamed_files

