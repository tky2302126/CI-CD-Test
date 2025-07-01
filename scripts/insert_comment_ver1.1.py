import sys
import datetime
from git import Repo
from pathlib import Path

REPO = Repo(".")
DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
LAST_COMMIT_MSG = REPO.head.commit.message.strip().replace('\n', ' ')
HISTORY_LINE_TEMPLATE = "// @history : {} {}\n"

def insert_or_update_comment(file_path: Path, username: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated = False
    history_line = HISTORY_LINE_TEMPLATE.format(DATE_STR, LAST_COMMIT_MSG)

    # すでにコメントがある場合は @history のみ更新
    if any("@author" in line for line in lines):
        for i, line in enumerate(lines):
            if "@history" in line:
                lines[i] = history_line
                updated = True
                break
    else:
        # 新規ファイル（ヘッダを挿入）
        header = [
            f"// @author : {username}\n",
            f"// @date : {DATE_STR}\n",
            history_line,
            "\n"
        ]
        lines = header + lines
        updated = True

    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

def main():
    if len(sys.argv) < 3:
        print("Usage: python insert_comment.py <changed_files.txt> <username>")
        sys.exit(1)

    changed_files_path = sys.argv[1]
    username = sys.argv[2]

    with open(changed_files_path, 'r', encoding='utf-8') as f:
        files = [line.strip() for line in f.readlines()]

    for file in files:
        path = Path(file)
        if path.suffix in ['.cpp', '.h'] and path.exists():
            insert_or_update_comment(path, username)

if __name__ == "__main__":
    main()
