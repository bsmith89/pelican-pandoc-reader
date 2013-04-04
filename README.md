
Pandoc reader plugin for Pelican
================================

This plugin for the [Pelican](https://github.com/getpelican/pelican) static site
generator adds support for parsing input files with [pandoc](https://github.com/jgm/pandoc).

In order to use the plugin, it has to be loaded with the Pelican plugin mechanism.

There are two settings that control which files are processed by pandoc, and how pandoc processes them.

    PANDOC_FILES = ['txt']
    PANDOC_ARGS = [
      '--mathjax',
      '--smart',
      '--toc',
      '--toc-depth=2',
      '--number-sections',
    ]

Do not forget to add the extensions in `PANDOC_FILES` to the `MARKUP` setting, so that Pelican processes the file types.

If pandoc is not found on your path, you can specify it in the settings as well.

    PANDOC_PATH = '/path/to/pandoc'

If the table of contents are requested with the `--toc` or `--table-of-contents` argument, it is parsed into the `toc` Pelican metadata field.
