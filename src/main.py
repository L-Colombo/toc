# TODO: improve documentation and help messages
import sys

import click
import toml

from toc.generate import gen_toc
from toc.io import read_toc, write_toc
from toc.meta import dump_toml, extract_meta
from toc.parser import parse_toc
from toc.utils import dump_toc, open_pdf, pprint_toc


@click.group()
def main():
    """
    toc - a CLI utility to edit the table of contents of your PDFs
    """
    pass


@click.command()
@click.argument("path-in", required=True)
@click.argument("recipe-file", required=True)
@click.option("--readable", "readable", is_flag=True)
@click.option("--vpos", "vpos", is_flag=True)
def gen(
    path_in,
    recipe_file,
    readable,
    vpos,
):
    """
    Generate a data.toc file from recipe.toml
    """

    try:
        with open_pdf(path_in) as doc:
            recipe = toml.load(recipe_file)
            toc = gen_toc(doc, recipe)

            if readable:
                print(pprint_toc(toc))
            else:
                print(dump_toc(toc, vpos), end="")

    except ValueError as e:
        raise e

        print("error:", e, file=sys.stderr)

        sys.exit(1)

    except IOError as e:
        raise e

        print("error: unable to open file", file=sys.stderr)
        print(e, file=sys.stderr)

        sys.exit(1)

    except KeyboardInterrupt as e:
        raise e

        print("error: interrupted", file=sys.stderr)

        sys.exit(1)


@click.command()
@click.argument("path_in", required=True)
@click.argument("toc_file", required=True)
@click.argument("out", required=True)
@click.option("--readable", "readable", is_flag=True)
@click.option("--print-toc", "print_toc", is_flag=True)
@click.option("--debug", "debug", is_flag=True)
@click.option("--vpos", "vpos", is_flag=True)
def io(path_in, toc_file, out, readable, print_toc, debug, vpos):
    """
    Read the data.toc file and write table of contents to a pdf
    """

    try:
        with open_pdf(path_in) as doc:
            if print_toc:
                toc = read_toc(doc)

                if readable:
                    print(pprint_toc(toc))
                else:
                    print(dump_toc(toc, vpos), end="")
                sys.exit(0)

            toc = parse_toc(toc_file)
            write_toc(doc, toc)

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
@click.option("--ignore-case", "ignore_case", is_flag=True)
@click.option("--level", "level", type=int, default=1)
@click.option("--no-recipe", is_flag=True)
def meta(path_in, page, pattern, level, ignore_case, no_recipe):
    """
    Extract metadata from a PDF and write them to a recipe.toml file
    """

    with open_pdf(path_in) as doc:
        meta = extract_meta(doc, pattern, page, ignore_case)

        # nothing found
        if len(meta) == 0:
            sys.exit(1)

        if no_recipe:
            print("\n".join([dump_toml(m, level) for m in meta]))
        else:
            with open("recipe.toml", "a") as recipe:
                recipe.write("\n".join([dump_toml(m, level) for m in meta]))
                # this is for padding in case of multiple runs
                recipe.write("\n")


main.add_command(gen)
main.add_command(io)
main.add_command(meta)

if __name__ == "__main__":
    main()
