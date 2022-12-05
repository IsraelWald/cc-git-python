import sys
import os
import zlib


def cat_file(args):
    folder = args[:2]
    filename = args[2:]
    fp = os.path.join(".git", "objects", folder, filename)
    with open(fp, "rb") as f:
        content = zlib.decompress(f.read())
        _, content = content.split(b'\x00')
        print(content.decode('utf-8'), end="")


def main():
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")
    elif command == "cat-file":
        cat_file(sys.argv[3])

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
