import os
import sys
from typing import TextIO

import click
import toml

from tocgen.generate import gen_toc
from tocgen.io import read_toc, write_toc
from tocgen.meta import dump_toml, extract_meta, print_meta
from tocgen.parser import parse_toc
from tocgen.utils import dump_toc, open_pdf, pprint_toc


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
@click.argument("path_in", required=True)
@click.argument("toc_file", required=True)
@click.argument("out", required=True)
@click.option("--readable", "readable", is_flag=True, flag_value=False)
@click.option("--print-toc", "print_toc", is_flag=True, flag_value=False)
@click.option("--debug", "debug", is_flag=True, flag_value=False)
@click.option("--vpos", "vpos", is_flag=True, flag_value=False)
def io(path_in, toc_file, out, readable, print_toc, debug, vpos):
    """
    Read the data.toc file and write table of contents to a pdf
    """
    try:
        with open_pdf(path_in) as doc:
            if toc_file.isatty() or print_toc:
                # no input from user, switch to output mode and extract the toc
                # of pdf
                toc = read_toc(doc)
                if len(toc) == 0:
                    print("error: no table of contents found", file=sys.stderr)
                    sys.exit(1)

                stdout = io.TextIOWrapper(
                    sys.stdout.buffer, encoding="utf-8", errors="ignore"
                )

                if readable:
                    print(pprint_toc(toc), file=stdout)
                else:
                    print(dump_toc(toc, vpos), end="", file=stdout)
                sys.exit(0)

            # an input is given, so switch to input mode
            toc = parse_toc(toc_file)
            write_toc(doc, toc)

            if out is None:
                # add suffix to input name as output
                pfx, ext = os.path.splitext(path_in)
                out = f"{pfx}_out{ext}"
            doc.save(out)
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
    except IndexError as e:
        if debug:
            raise e
        print("index error:", e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt as e:
        if debug:
            raise e
        print("error: interrupted", file=sys.stderr)
        sys.exit(1)


@click.command()
@click.argument("path_in", required=True)
@click.argument("page", required=True, type=int)
@click.argument("pattern", required=True)
@click.option("--level", "level", type=int, default=1)
@click.option("--ignore-case", "ignore_case", is_flag=True, flag_value=False)
def meta(path_in, page, pattern, level, ignore_case):
    """
    Extract metadata from a PDF and write them to a recipe.toml file
    """

    with open_pdf(path_in) as doc:
        meta = extract_meta(doc, pattern, page, ignore_case)

        # nothing found
        if len(meta) == 0:
            sys.exit(1)

        print("\n".join([dump_toml(m, level) for m in meta]))


main.add_command(gen)
main.add_command(io)
main.add_command(meta)

if __name__ == "__main__":
    main()
