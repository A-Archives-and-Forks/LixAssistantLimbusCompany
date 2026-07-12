"""
这是个汉化过程中的小工具
复制一份ego图片全集，用这个程序尝试给所有ego命名，那么那些命名失败的就是存在拼写错误等各种玄学问题 需要手动调整汉化配置的
"""

import os, json

def rename_all(root, mapping):
    for dirpath, _, files in os.walk(root):
        for f in files:
            name, ext = os.path.splitext(f)
            if name in mapping:
                old = os.path.join(dirpath, f)
                new = os.path.join(dirpath, mapping[name] + ext)
                os.rename(old, new)

# 使用示例
if __name__ == "__main__":
    with open(r"../config/language/zh/ego_gifts.json", 'r', encoding = 'utf8') as f:
        mapping = json.load(f)
    rename_all(r"..\img\temp\ego_gifts", mapping)
