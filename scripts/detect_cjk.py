import sys
import re
import os

CJK_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff\uac00-\ud7af]')

def file_contains_cjk(filepath, report):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if CJK_RE.search(line):
                    report.append((filepath, i, line.strip()))
    except Exception as e:
        pass

def scan_dir(path, report, exts=None):
    for root, dirs, files in os.walk(path):
        for file in files:
            if exts:
                if not any(file.lower().endswith(ext) for ext in exts):
                    continue
            file_path = os.path.join(root, file)
            file_contains_cjk(file_path, report)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python detect_cjk.py <file_or_dir> [ext1,ext2,...]")
        sys.exit(1)
    target = sys.argv[1]
    exts = None
    if len(sys.argv) > 2:
        exts = tuple(ext.strip().lower() for ext in sys.argv[2].split(','))
    report = []
    if os.path.isdir(target):
        scan_dir(target, report, exts)
    else:
        file_contains_cjk(target, report)
    if report:
        print("CJK characters found:")
        for filepath, lineno, line in report:
            print(f"{filepath} (line {lineno}): {line}")
    else:
        print("No CJK characters found.")
