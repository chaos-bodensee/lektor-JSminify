# JSminify
[![PyPI version](https://badge.fury.io/py/lektor-jsminify.svg)](https://badge.fury.io/py/lektor-jsminify)

JS minifier for Lektor that automatically minifies javascript files

Uses [rjsmin](https://pypi.org/project/rjsmin/)  and looks for .js files,
minifying them as part of the build process.

## Installing

You can install the plugin with Lektor's installer::
```bash
lektor plugins add lektor-jsminify
```

Or by hand, adding the plugin to the packages section in your lektorproject file::
```bash
[packages]
lektor-jsminify = 1.2
```

## Usage
#####

To enable jsminify, pass the `jsminify` flag when starting the development
server or when running a build::
```bash
lektor build -f jsminify
```

When the flag is present, jsminify will take all .js files from asset_sources/js, minifies them and places them
in assets/js.


The Plugin has the following settings you can adjust to your needs:

|parameter      |default value      |description                                                                                       |
|---------------|-------------------|--------------------------------------------------------------------------------------------------|
|source_dir     |asset_sources/js/| the directory in which the plugin searchs for js files (subdirectories are included)           |
|output_dir     |assets/js/        | the directory the minified js files get place at                                                |
|name_prefix      |                  | prefix for output name e.g. test.scss gets to test<name_prefix>.css                                                                         |
|keep_bang_comments|False              | keep comments starting with an exclamation mark                                                     |

An example file with the default config can be found at `configs/jscompile.ini`
