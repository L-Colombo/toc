Toc - a CLI utility to to edit the table of contents of your PDFs
===============

Toc is a small command line utility to edit the table of contents of pdf files.

This application and much of its code is a reworking of [pdf.tocgen](https://github.com/Krasjet/pdf.tocgen), to whom goes all the credits.

**NB**: This is not a drop-in replacement of `pdf.tocgen`!
Although the idea and most of the code are taken from `pdf.tocgen`, and the workflow is very similar, the API and the overall usage are different.
Please, see below.

# Usage

``` bash
$ toc [SUBCOMMAND] <OPTIONS>
```

## Workflow

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

``` bash
$ toc gen 
```
### `io`

``` bash
$ toc io
```

### `meta`

``` bash
$ toc meta
```

## Auxiliary file format reference
