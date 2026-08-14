import sys
from typing import TextIO

import click
import toml

from lib.generate import gen_toc
from lib.utils import dump_toc, open_pdf, pprint_toc


@click.group()
def cli():
    """
    The main entrypoint
    """
    pass


@click.command()
@click.argument("path_in")
@click.argument("recipe_file")
@click.option("--readable", "-r")
@click.option("--debug", "-d")
@click.option("--vpos", "-V")
def gen(
    path_in,
    recipe_file,
    debug,
    readable,
    vpos,
):
    """
    Generate a data.toc file from recipe.toml
    """

    out: TextIO = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="ignore")

    try:
        with open_pdf(path_in) as doc:
            recipe = toml.load(recipe_file)
            toc = gen_toc(doc, recipe)
            if readable:
                print(pprint_toc(toc), file=out)
            else:
                print(dump_toc(toc, vpos), end="", file=out)
    except ValueError as e:
        if debug:
            raise e
        print("error:", e, file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        if debug:
            raise e
        print("error: unable to open file", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt as e:
        if debug:
            raise e
        print("error: interrupted", file=sys.stderr)
        sys.exit(1)


@click.command()
def io():
    """
    Read the data.toc file and write table of contents to a pdf
    """
    pass


@click.command()
def meta():
    """
    Extract pdf metadata to a recipe.toml
    """
    pass


cli.add_command(gen)
cli.add_command(io)
cli.add_command(meta)

if __name__ == "__main__":
    cli()
