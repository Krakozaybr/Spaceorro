import os

cur_dir = os.path.dirname(__file__)
ways = [cur_dir]
total = 0
without_spaces = 0

banned_dirs = ["data", "venv"]

while ways:
    filename = ways.pop()
    if (
        os.path.isfile(filename)
        and filename.endswith(".py")
        and not filename.endswith("check_lines_of_code.py")
    ):
        with open(filename, "r", encoding="utf-8") as r:
            comment_now = False
            for line in r.readlines():
                l = line.strip()
                if not comment_now and l.startswith('"""'):
                    comment_now = True
                elif comment_now and l.endswith('"""'):
                    comment_now = False
                    without_spaces -= 1
                if (
                    l
                    and not l.startswith("#")
                    and not comment_now
                    and not (l.startswith("import") or l.startswith("from"))
                ):
                    without_spaces += 1
                total += 1
    elif os.path.isdir(filename) and os.path.basename(filename) not in banned_dirs:
        files = os.listdir(filename)
        for file in files:
            ways.append(os.path.join(filename, file))

print(f"Непустые строки кода (без импортов): {without_spaces}")
print(f"Всего: {total}")
