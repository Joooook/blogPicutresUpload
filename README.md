# md图片自动上传smms图床
博客园上传图片太麻烦了，于是就写了一个上传smms的小脚本

在smms中获取token之后

headers={'Authorization':把你的token复制进来}


## usage
```
python upload.py -f 你的md文件.md
```

脚本会在原md文件的目录下生成一个output文件夹，新的md文件会放在那里。


