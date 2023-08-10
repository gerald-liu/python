import os

valid_ext = ['.zip', '.7z']


def get_target_ext(old_ext: str, valid_ext: list[str]) ->str:
    
    for ext in valid_ext:
        if old_ext[:len(ext)] == ext:
            return ext

    return old_ext


for file_basename in os.listdir():

    filename, ext = os.path.splitext(file_basename)

    new_ext = get_target_ext(ext, valid_ext)

    os.rename(file_basename, f'{filename}{new_ext}')
