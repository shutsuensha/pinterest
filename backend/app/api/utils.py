import shutil

def save_image(image_path, file):
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file, new_file)