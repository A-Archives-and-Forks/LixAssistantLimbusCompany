"""
这是个生成汉化文件的小工具
生成出来还要再调整一下，原因是英文OCR结果存在识别错误的情况，必须将错就错，借助rename_egogift.py等工具或者强大的意志力改一改
其实最好把ego gift的管理彻底重构一下，但是我还是选择了再拉一坨
AI写代码真是太好用了
"""

import json
import os
import re
from pathlib import Path


def extract_name(item):
    """提取名称并去除+后缀"""
    name = item.get('name', '')
    if name:
        # 去除 + 后缀 (如 "炼狱炎蝶之梦++" -> "炼狱炎蝶之梦")
        name = re.sub(r'\++$', '', name)
    return name


def get_names_from_file(file_path):
    """从单个JSON文件获取所有名称（去除后缀后）"""
    names = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict) and 'dataList' in data:
            items = data['dataList']
        elif isinstance(data, list):
            items = data
        else:
            return names

        for item in items:
            name = extract_name(item)
            if name:
                names.append(name)
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    return names


def build_mapping(cn_dir, en_dir, output_path):
    """
    构建中英文名称映射，输出 {en: cn, ...} 格式
    """
    cn_file_groups = {}  # 文件名 -> 中文名称列表
    en_file_groups = {}  # 文件名 -> 英文名称列表
    mapping = {}

    # 处理中文目录下的所有JSON文件
    print(f"正在处理中文目录: {cn_dir}")
    # cn_files = list(Path(cn_dir).glob('EGOgift_MirrorDungeon*.json'))
    # cn_files.extend(list(Path(cn_dir).glob('*EGOgift_MirrorDungeon*.json')))
    cn_files = list(Path(cn_dir).glob('EGOgift*.json'))
    cn_files.extend(list(Path(cn_dir).glob('*EGOgift*.json')))

    for file_path in cn_files:
        print(f"  读取: {file_path.name}")
        names = get_names_from_file(file_path)
        # 用去除前缀后的名字作为key
        # key = file_path.stem.replace('EGOgift_MirrorDungeon', '').replace('_', '')
        key = file_path.stem.replace('EGOgift', '').replace('_', '')

        if not key:
            key = 'default'
        cn_file_groups[key] = names

    # 处理英文目录下的所有JSON文件
    print(f"\n正在处理英文目录: {en_dir}")
    # en_files = list(Path(en_dir).glob('EN_EGOgift_MirrorDungeon*.json'))
    # en_files.extend(list(Path(en_dir).glob('*EN_EGOgift_MirrorDungeon*.json')))
    en_files = list(Path(en_dir).glob('EN_EGOgift*.json'))
    en_files.extend(list(Path(en_dir).glob('*EN_EGOgift*.json')))

    for file_path in en_files:
        print(f"  读取: {file_path.name}")
        names = get_names_from_file(file_path)
        # key = file_path.stem.replace('EN_EGOgift_MirrorDungeon', '').replace('_', '')
        key = file_path.stem.replace('EN_EGOgift', '').replace('_', '')

        if not key:
            key = 'default'
        en_file_groups[key] = names

    # 匹配相同key的文件
    all_keys = set(cn_file_groups.keys()) & set(en_file_groups.keys())

    if not all_keys:
        print("\n警告: 没有找到匹配的文件对！")
        print(f"中文文件keys: {list(cn_file_groups.keys())}")
        print(f"英文文件keys: {list(en_file_groups.keys())}")

    for key in all_keys:
        cn_list = cn_file_groups[key]
        en_list = en_file_groups[key]

        # 按名称长度或字母顺序排序使配对更稳定
        # 由于名称顺序应该一致，直接按顺序配对
        min_len = min(len(cn_list), len(en_list))

        for i in range(min_len):
            if cn_list[i] and en_list[i]:
                mapping[en_list[i]] = cn_list[i]

        # 如果长度不匹配，打印警告
        if len(cn_list) != len(en_list):
            print(f"  警告: 文件 {key} 中英文数量不匹配: CN={len(cn_list)}, EN={len(en_list)}")

    mapping = dict(sorted(mapping.items()))

    # 保存结果（纯对象，无多余字段）
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"\n映射已保存到: {output_path}")
    print(f"共匹配了 {len(mapping)} 个E.G.O饰品名称")

    return mapping


if __name__ == "__main__":
    # 请修改为你的实际路径
    cn_dir = r"F:\SteamLibrary\steamapps\common\Limbus Company\LimbusCompany_Data\Lang\LLC_zh-CN"  # 中文JSON文件所在目录
    en_dir = r"F:\SteamLibrary\steamapps\common\Limbus Company\LimbusCompany_Data\Assets\Resources_moved\Localize\en"  # 英文JSON文件所在目录
    output_path = r"../config/language/zh/ego_gifts.json"  # 输出文件路径

    # 检查目录是否存在
    if not os.path.exists(cn_dir):
        print(f"警告: 中文目录 {cn_dir} 不存在")
    if not os.path.exists(en_dir):
        print(f"警告: 英文目录 {en_dir} 不存在")

    mapping = build_mapping(cn_dir, en_dir, output_path)

    # 打印部分结果
    print("\n部分映射示例:")
    for i, (en, cn) in enumerate(list(mapping.items())[:10]):
        print(f"  \"{en}\": \"{cn}\"")
    if len(mapping) > 10:
        print(f"  ... 还有 {len(mapping) - 10} 个")