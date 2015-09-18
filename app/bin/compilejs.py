#coding: utf-8
import os

def get_files(folder, ignores=[]):
    ignores.append('compile.js')
    if not os.path.isdir:
        raise Exception('文件目录不存在')
    files = os.listdir(folder)
    for file in ignores:
        if file in files:
            files.remove(file)
    res = []
    for file in files:
        file = os.path.join(folder, file)
        if os.path.isdir(file):
            res.extend(get_files(file))
        else:
            res.append(file)
    return res

def compile(folder, ignores=[]):
    compile_file = os.path.join(folder, 'compile.js')
    if os.path.isfile(compile_file):
        os.remove(compile_file)
    files = get_files(folder, ignores)
    new_file = os.path.join(folder, 'compile.js')
    with open(new_file, 'a') as f:
        for file in files:
            with open(file, 'r') as rf:
                content = rf.read()
                f.write(content)
                print(file + ' success')