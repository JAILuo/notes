#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# extract_toc.py - 提取 Markdown 标题生成目录（支持多编码）

import sys
import locale
import re

def extract_toc(filename):
    """
    尝试多种编码读取 markdown 文件，提取标题行，返回带缩进的目录列表。
    忽略代码块内的内容，只匹配标准标题（# 后必须跟空格）。
    """
    encodings = [
        'utf-8-sig',
        'utf-8',
        locale.getpreferredencoding(),
        'gbk',
        'gb18030'
    ]

    # 匹配标题：行首可有前导空白，然后是1~6个#，再至少一个空白，然后是标题文本
    header_re = re.compile(r'^(\s*)(#{1,6})\s+(.*)$')

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                toc_lines = []
                in_code_block = False
                for line in f:
                    stripped = line.strip()
                    # 检测代码块开始/结束（忽略语言标识）
                    if stripped.startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        continue

                    m = header_re.match(line)
                    if not m:
                        continue
                    indent, hashes, title = m.groups()
                    level = len(hashes)          # 标题级别
                    # 保留原始缩进（如果行首有缩进）当作额外的层次？通常标题不在缩进内，但可以保留
                    # 我们按标准缩进：每级2个空格
                    indentation = '  ' * (level - 1)
                    # 如果原始有缩进，也可以叠加，这里简单采用标准缩进
                    toc_lines.append(indentation + title)
                return toc_lines
        except UnicodeDecodeError:
            continue
        except Exception:
            raise

    raise UnicodeDecodeError(f"无法以任何尝试的编码读取文件: {filename}")

def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <markdown文件>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    try:
        toc = extract_toc(filename)
    except FileNotFoundError:
        print(f"错误: 文件 '{filename}' 不存在", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"错误: 无法解码文件 '{filename}'，请确认编码。详细信息: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)

    print("```txt")
    for line in toc:
        print(line)
    print("```")

if __name__ == "__main__":
    main()