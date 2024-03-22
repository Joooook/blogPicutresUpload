import argparse
import os
import os.path
import re

import requests

uploaded_images_dict = {}


def upload(path:str,abspath: str) -> bool:
    """
    上传图片
    :param path: the path written in .md file
    :param abspath: the abs path of the image
    :return:
    """
    global uploaded_images_dict
    headers={'Authorization':''}
    files = {'smfile':open(abspath,'rb')}
    url='https://sm.ms/api/v2/upload'
    res=requests.post(url,headers=headers,files=files).json()
    suc=res['success']
    if suc:
        newpath=res['data']['url']
    else:
        message=res['message']
        print(f"[?] {message}")
        if 'image exists' in message:
            newpath=res['images']
        else:
            newpath=abspath
    uploaded_images_dict[path] = newpath
    return True


def parse_images(filepath: str) -> list:
    """
    解析md中的图片地址
    :param filepath: .md file path
    :return images_path: if success
    """
    try:
        f = open(filepath, 'r')
    except FileNotFoundError as e:
        print(f'[-] {e}')
        return []
    print(f'[+] parse {filepath}')
    images_path = []
    for line in f:
        res = re.findall(r'!\[]\(<(.+)>\)', line)
        if res:
            images_path += res
    f.close()
    return images_path


def rewrite(filepath: str) -> bool:
    """
    重写md
    :param filepath:
    :return:
    """
    global uploaded_images_dict
    try:
        f = open(filepath, 'r')
    except FileNotFoundError as e:
        print(f'[-] {e}')
        return False
    output_dirpath = os.path.abspath(os.path.join(filepath, '../output'))
    if not os.path.exists(output_dirpath):
        os.mkdir(output_dirpath)
    o = open(os.path.join(output_dirpath, os.path.basename(filepath)),'w')
    for line in f:
        res = re.findall(r'!\[]\(<(.+)>\)', line)
        if res:
            new_path = uploaded_images_dict[res[0]]
            line = re.sub(r'!\[]\(<(.+)>\)', f'![](<{new_path}>)', line)
        o.write(line)
    f.close()
    o.close()
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='blog pictures upload')
    parser.add_argument('-f', '--file', type=str)
    args = parser.parse_args()
    filepath = os.path.abspath(args.file)
    images_path = parse_images(filepath)
    dirpath = os.path.abspath(os.path.join(filepath, '../'))
    for path in images_path:
        image_path = os.path.abspath(os.path.join(dirpath, path))
        if upload(path, image_path):
            print(f'[+] Upload {image_path} success')
        else:
            raise Exception('[-] File upload failed, path:' + image_path)
    print(f'[+] All images uploaded')
    print(f'[+] Rewrite .md file')
    if rewrite(filepath):
        print(f'[+] Successfully rewrite .md file')
    else:
        raise Exception('[-] Failed to rewrite .md file')
