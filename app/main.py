import sys
import os
import zlib
import click
import hashlib
from pathlib import Path


@click.Group
def cli():
    print("PyGit")


@cli.command("init")
def init():
    os.mkdir(".git")
    os.mkdir(os.path.join(".git", "objects"))
    os.mkdir(os.path.join(".git", "refs"))
    os.mkdir(os.path.join(".git", "HEAD"))
    with open(os.path.join(".git", "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    click.secho("Initialized .git directory", fg="green")


@cli.command("cat-file")
@click.option("-p")
def cat_file(**kwargs):
    args = kwargs['p']
    folder = args[:2]
    filename = args[2:]
    fp = os.path.join(".git", "objects", folder, filename)
    with open(fp, "rb") as f:
        content = zlib.decompress(f.read())
        _, content = content.split(b'\x00')
        click.echo(content.decode('utf-8'), nl=False)


@cli.command("hash-object")
@click.option("-w")
def hash_object(**kwargs):
    filename = kwargs["w"]
    with open(filename, "r") as f:
        obj = f.read()
    formatted_obj = bytes(f"blob {bytes(str(len(obj)), 'utf-8')}\x00{obj}",
                          "utf-8")
    compressed = zlib.compress(formatted_obj)
    hashed = hashlib.sha1(formatted_obj).hexdigest()

    obj_dir = hashed[:2]
    obj_file = hashed[2:]
    objects = Path(".git") / Path("objects")
    Path(objects / Path(obj_dir)).mkdir(exist_ok=True)
    Path(objects / Path(obj_dir) / Path(obj_file)).write_bytes(compressed)

    click.echo(hashed, nl=False)


if __name__ == "__main__":
    cli()
