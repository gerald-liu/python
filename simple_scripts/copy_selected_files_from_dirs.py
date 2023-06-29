import os
import shutil
import sys

home_path = 'F:\\LWY\\OneDrive - HKUST Connect\\Abama\\新股'
target_path = "F:\\Upload\\新股研究"
author_name = sys.argv[1]

def get_target_basename(filename, ext, author):
    return filename + '_' + author + ext

def is_file1(filename, ext):
    return ext == '.pdf' and '研究报告' in filename and len(filename) <= 8

def is_file2(filename):
    return '初稿' in filename or '新股介绍' in filename

for home_item in os.scandir(home_path):
    
    if home_item.is_dir():
        folder_path = home_item.path
        folder_name = os.path.basename(folder_path)
        
        target_folder_path = os.path.join(target_path, folder_name)
        
        for folder_item in os.scandir(folder_path):
            if folder_item.is_file():
                file_path = folder_item.path
                file_basename = os.path.basename(file_path)
                filename, ext = os.path.splitext(file_basename)
                
                if is_file1(filename, ext) or is_file2(filename):
                    if not os.path.exists(target_folder_path):
                        os.makedirs(target_folder_path)
                    target_file_path = os.path.join(target_folder_path, get_target_basename(filename, ext, author_name))
                    shutil.copy(file_path, target_file_path)
    