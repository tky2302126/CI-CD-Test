import os
import datetime
from git import Repo

REPO = Repo(".")
USERNAME = os.getenv("GITHUB_ACTOR", "unknown-user")
DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
LAST_COMMIT_MSG = REPO.head.commit.message.strip().replace('\n', ' ')
HISTORY_LINE = f"// @history : {DATE_STR} {LAST_COMMIT_MSG}\n"

def insert_or_update_comment(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated = False

    # すでにコメントがある場合は @history のみ更新
    if any("@author" in line for line in lines):
        for i, line in enumerate(lines):
            if "@history" in line:
                lines[i] = HISTORY_LINE
                updated = True
                break
    else:
        # 新規ファイル（ヘッダを挿入）
        header = [
            f"// @author : {USERNAME}\n",
            f"// @date : {DATE_STR}\n",
            HISTORY_LINE,
            "\n"
        ]
        lines = header + lines
        updated = True

    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

def walk_cpp_files():
    for root, _, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".cpp") or file.endswith(".h"):
                insert_or_update_comment(os.path.join(root, file))

if __name__ == "__main__":
    walk_cpp_files()
