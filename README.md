Toc - a CLI utility to to edit the table of contents of your PDFs
===============

Toc is a small command line utility to edit the table of contents of pdf files.

This application and much of its code is a reworking of [pdf.tocgen](https://github.com/Krasjet/pdf.tocgen), to whom goes all the credits.

**NB**: This is not a drop-in replacement of `pdf.tocgen`!
Although the idea and most of the code are taken from `pdf.tocgen`, and the workflow is very similar, the API and the overall usage are different.
Please, see below.

# Usage

``` bash
$ toc [OPTIONS] COMMAND [ARGS]
```

# Workflow

The general workflow is essentially that of `pdf.tocgen`.

1. The first step is to use the `meta` subcommand to generate a `recipe.toml` file.
The `recipe.toml` file contains metadata about elements fond in the PDF that help identify chapter, sections, and other points at which you want to create an entry in the table of contents

2. In the second step, calling the `gen` subcommand, the `recipe.toml` file is read, the pdf file is parsed, and `data.toc` file is generated.
The `data.toc` file contains the title of the table of contents entry and the page of the document at which that entry is.
Indentation is used to mark the level of entries.
**NB**: The two first steps can be skipped entirely and a `data.toc` can be generated manually - make sure it is formatted correctly (see the reference below).

3. Finally, using the `io` subcommand the table of contents defined in the `data.toc` file is written to the PDF file and saved.

## Subcommands

### `gen`

Generate a `data.toc` file from a `recipe.toml` file.

``` bash
$ toc gen [OPTIONS] PATH_IN RECIPE_FILE
```

`PATH_IN` is the PDF file for which the table of content is to be created.

`RECIPE_FILE` is the `recipe.toml` file generated with the `meta` subcommand.

### `io`

Write the table of contents specified in a `data.toc` file to the PDF.

``` bash
$ toc io [OPTIONS] PATH_IN TOC_FILE OUT
```

`PATH_IN` is the PDF file for which the table of content is to be created.

`TOC_FILE` is the `data.toc` file, which contains the structure of the table of contents to be written.

`OUT` is name of the PDF file to be produced, which is a copy of the original PDF file, with the added table of contents.
Note that this command is non-destructive: the original PDF remains unchanged (useful in case there are problems or the end result is not what the user intended).

### `meta`

``` bash
$ toc meta [OPTIONS] PATH_IN PAGE PATTERN
```

`PATH_IN` is the PDF file to be scanned.

`PAGE` is the page where `PATTERN` is to be searched.

**EXAMPLE**: If I want get the metadata of font title of chapters in `my-cool.pdf` file, I can open the file, see that the first chapter is at, say, page 7 and is titled `my cool first chapter`, I will run

``` bash
$ toc meta my-cool.pdf 7 "My cool first chapter"
```

Unless the `--ignore-case` flag is passed, the search for `PATTERN` is case sensitive.

It is assumed that the search matches a first-level entry.
You can specify a different level passing `--level=X`, where `X` is a positive integer greater than one.

## Auxiliary file format reference

### `recipe.toml`

This is a toml file which contains information about the fonts of sections to be extracted in order to generate automatically the `data.toc` file.

**IMPORTANT**: to avoid compatibility problems, it is advisable **NOT** to change this file manually.

### `data.toc`

This file is in a dialect of a CSV, where one blank space acts as the separator.

Levels in the table of contents are expressed with indentation: no indentation means first level, one tab means second level, and so on.

The first field (in double quotes) is the title of the table of contents entry, the table field is the page of the table of contents.
**NB**: the page is the page **of the document**, not of the text.
You should not merely translate the table of contents page of your book; you should also count the leading front matter, colophon, etc.

Example:

``` cvs
"Cover page" 1
"Table of Contents" 2
"First Chapter" 7
    "A subsesction of the first chapter" 12
    "Another subsection of the first chapter" 15
"Second Chapter" 22
"Bibliography" 33
```
