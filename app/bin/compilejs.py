#coding: utf-8
import os

def get_files(folder, includes=[]):
    res = []
    if not includes:
        includes = os.listdir(folder)
    for file in includes:
        file_or_folder = os.path.join(folder, file)
        if os.path.isdir(file_or_folder):
            res.extend(get_files(file_or_folder))
        else:
            res.append(file_or_folder)
    return res

def compile(folder, includes=[]):
    compile_file = os.path.join(folder, 'compile.js')
    if os.path.isfile(compile_file):
        os.remove(compile_file)
    files = get_files(folder, includes)
    new_file = os.path.join(folder, 'compile.js')
    with open(new_file, 'a') as f:
        for file in files:
            with open(file, 'r') as rf:
                content = rf.read()
                # content = content\
                #     .replace('function ', '***function***')\
                #     .replace('var ', '***var***')\
                #     .replace('return ', '***return***')\
                #     .replace(' ', '')\
                #     .replace('***function***', 'function ')\
                #     .replace('***var***', 'var ')\
                #     .replace('***return***', 'return ')\
                #     .replace('usestrict', 'use strict')
                f.write(content)
                print(file + ' success')