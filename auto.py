import os

DEFAULT_FILE = "404_mkdocs_excluded.md"
DEFAULT_FILE_PATH = "MkDocs/404_mkdocs_excluded.md"


def list_files(startpath):
    nav_structure = {}
    exclude_files = ['mkdocs_excluded','.DS_Store', 'auto.py', 'nav_structure.md', 'mkdocs.yml', 'home_index.md', 'new_mkdocs.yml']
    exclude_dirs = ['mkdocs_excluded','OnePiece_Pictures']

    for root, dirs, files in os.walk(startpath):
        # 过滤掉不需要的文件
        files = [f for f in files if f not in exclude_files]
        # 过滤掉包含特定子字符串的文件夹
        dirs[:] = [d for d in dirs if not any(ex in d for ex in exclude_dirs)]

        # 对文件和文件夹进行排序
        files.sort()
        dirs.sort()

        # 获取相对路径
        relative_path = os.path.relpath(root, startpath)
        # 获取当前文件夹层级
        levels = relative_path.split(os.sep)

        # 构建嵌套字典
        current_level = nav_structure
        for level in levels:
            if level == '.':
                continue
            if level not in current_level:
                current_level[level] = {}
            current_level = current_level[level]

        # 添加文件到当前层级
        for file in files:
            current_level[file] = os.path.join(relative_path, file)

        # 如果没有文件，添加默认文件
        if not files and not dirs:
            current_level["404"] = DEFAULT_FILE_PATH

    return nav_structure

def format_nav(nav_dict, indent_level=1):
    formatted_nav = ""
    indent = '  ' * indent_level  # 根据indent_level生成适当数量的缩进
    for key, value in sorted(nav_dict.items()):
        if isinstance(value, dict):
            formatted_nav += f'{indent}- \'{key}\':\n'  # 如果是目录，增加缩进并递归调用
            formatted_nav += format_nav(value, indent_level + 1)
        else:
            formatted_nav += f'{indent}- \'{key}\': {value}\n'  # 如果是文件，直接添加条目
    return formatted_nav

if __name__ == "__main__":
    # 获取脚本所在的目录路径
    directory_path = os.path.dirname(os.path.abspath(__file__))
    nav_structure = list_files(directory_path)
    
    # title
    nav_content = "site_name: Jeff Liu Lab's wiki\n\n"
    # nav(title+Home)
    nav_content += "nav:\n"
    nav_content += "  - \'Home\': /MkDocs/home_index.md\n"
    
    # nav(其余生成的部分)
    nav_content += format_nav(nav_structure, 1)
    # theme
    nav_content += "\n# 配置Material主题\ntheme:\n  name: 'material'\n"
    # plugins
    nav_content += "\nplugins:\n  - search # MkDocs内置搜索插件\n"
    nav_content += "  - awesome-pages \n  - autorefs # 自动链接不同词条\n"
    # markdown_extensions
    nav_content += "\nmarkdown_extensions:\n  - toc:\n      permalink: true\n"
    
    # 输出到Markdown文件
    output_file = os.path.join(directory_path, "nav_structure.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(nav_content)
    
    print(f"生成的内容已保存到 {output_file}")


def rename_files(directory, old_name, new_name):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if old_name in file:
                old_file = os.path.join(root, file)
                new_file = os.path.join(root, file.replace(old_name, new_name))
                os.rename(old_file, new_file)
                print(f'Renamed: {old_file} -> {new_file}')

if __name__ == "__main__":
    # 获取脚本所在的目录路径
    directory_path = os.path.dirname(os.path.abspath(__file__))
    # 修改以下变量为你需要的旧名称和新名称
    old_name = "nav_structure.md"
    new_name = "mkdocs.yml"
    rename_files(directory_path, old_name, new_name)
