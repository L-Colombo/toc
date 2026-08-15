import sys
from typing import TextIO

import click
import toml

from lib.generate import gen_toc
from lib.utils import dump_toc, open_pdf, pprint_toc


@click.group()
def main():
    """
    toc - a CLI utility to edit the table of contents of your PDFs
    """
    pass


@click.command()
@click.argument("path in", required=True)
@click.argument("recipe file", required=True)
@click.option("--readable", "readable", is_flag=True, flag_value=False)
@click.option("--debug", "debug", is_flag=True, flag_value=False)
@click.option("--vpos", "vpos", is_flag=True, flag_value=False)
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


main.add_command(gen)
main.add_command(io)
main.add_command(meta)

if __name__ == "__main__":
    main()
