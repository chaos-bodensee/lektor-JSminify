# JSminify
[![PyPI version](https://badge.fury.io/py/lektor-jsprettify.svg)](https://badge.fury.io/py/lektor-jsprettify)

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
lektor-jsminify = 0.2
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

