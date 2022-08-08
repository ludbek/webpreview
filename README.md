# webpreview

For a given URL, `webpreview` extracts its **title**, **description**, and **image url** using
[Open Graph](http://ogp.me/), [Twitter Card](https://dev.twitter.com/cards/overview), or
[Schema](http://schema.org/) meta tags, or, as an alternative, parses it as a generic webpage.

<p>
    <a href="https://pypi.org/project/webpreview/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/webpreview"></a>
    <a href="https://pypi.org/project/webpreview/"><img alt="PyPI" src="https://img.shields.io/pypi/v/webpreview?logo=pypi&color=blue"></a>
    <a href="https://github.com/ludbek/webpreview/actions?query=workflow%3Atest"><img alt="Build status" src="https://img.shields.io/github/workflow/status/ludbek/webpreview/test?label=build&logo=github"></a>
    <a href="https://codecov.io/gh/ludbek/webpreview"><img alt="Code coverage report" src="https://img.shields.io/codecov/c/github/ludbek/webpreview?logo=codecov"></a>
</p>


## Installation

```shell
pip install webpreview
```

## Usage

Use the generic `webpreview` method (added in *v1.7.0*) to parse the page independent of its nature.
This method fetches a page and tries to extracts a *title, description, and a preview image* from it.

It first attempts to parse the values from **Open Graph** properties, then it falls back to
**Twitter Card** format, and then to **Schema**. If none of these methods succeed in extracting all
three properties, then the web page's content is parsed using a generic HTML parser.

```python
>>> from webpreview import webpreview

>>> p = webpreview("https://en.wikipedia.org/wiki/Enrico_Fermi")
>>> p.title
'Enrico Fermi - Wikipedia'
>>> p.description
'Italian-American physicist (1901–1954)'
>>> p.image
'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg'

# Access the parsed fields both as attributes and items
>>> p["url"] == p.url
True

# Check if all three of the title, description, and image are in the parsing result
>>> p.is_complete()
True

# Provide page content from somewhere else
>>> content = """
<html>
    <head>
        <title>The Dormouse's story</title>
        <meta property="og:description" content="A Mad Tea-Party story" />
    </head>
    <body>
        <p class="title"><b>The Dormouse's story</b></p>
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
    </body>
</html>
"""

# The the function's invocation won't make any external calls,
# only relying on the supplied content, unlike the example above
>>> webpreview("aa.com", content=content)
WebPreview(url="http://aa.com", title="The Dormouse's story", description="A Mad Tea-Party story")
```

### Using the command line

When `webpreview` is installed via `pip`, then the accompanying command-line tool is
installed alongside.

```shell
$ webpreview https://en.wikipedia.org/wiki/Enrico_Fermi
title: Enrico Fermi - Wikipedia
description: Italian-American physicist (1901–1954)
image: https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg

$ webpreview https://github.com/ --absolute-url
title: GitHub: Where the world builds software
description: GitHub is where over 83 million developers shape the future of software, together.
image: https://github.githubassets.com/images/modules/site/social-cards/github-social.png
```

### Using compatibility API

Before *v1.7.0* the package mainly exposed a different set of the API methods.
All of them are supported and may continue to be used.

```python
# WARNING:
# The API below is left for BACKWARD COMPATIBILITY ONLY.

from webpreview import web_preview
title, description, image = web_preview("aurl.com")

# specifing timeout which gets passed to requests.get()
title, description, image = web_preview("a_slow_url.com", timeout=1000)

# passing headers
headers = {'User-Agent': 'Mozilla/5.0'}
title, description, image = web_preview("a_slow_url.com", headers=headers)

# pass html content thus avoiding making http call again to fetch content.
content = """<html><head><title>Dummy HTML</title></head></html>"""
title, description, image = web_preview("aurl.com", content=content)

# specifing the parser
# by default webpreview uses 'html.parser'
title, description, image = web_preview("aurl.com", content=content, parser='lxml')
```

## Run with Docker

The docker image can be built and ran similarly to the command line.
The default entry point is the `webpreview` command-line function.

```shell
$ docker build -t webpreview .
$ docker run -it --rm webpreview "https://en.m.wikipedia.org/wiki/Enrico_Fermi"
title: Enrico Fermi - Wikipedia
description: Enrico Fermi (Italian: [enˈriːko ˈfermi]; 29 September 1901 – 28 November 1954) was an Italian (later naturalized American) physicist and the creator of the world's first nuclear reactor, the Chicago Pile-1. He has been called the "architect of the nuclear age"[1] and the "architect of the atomic bomb".
image: https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg
```

*Note*: built docker image weighs around 210MB.

## Testing

```shell
# Execute the tests
poetry run pytest webpreview

# OR execute until the first failed test
poetry run pytest webpreview -x
```

## Setting up development environment

```shell
# Install a correct minimal supported version of python
pyenv install 3.7.13

# Create a virtual environment
# By default, the project already contains a .python-version file that points
# to 3.7.13.
python -m venv .venv

# Install dependencies
# Poetry will automatically install them into the local .venv
poetry install

# If you have errors likes this:
ERROR: Can not execute `setup.py` since setuptools is not available in the build environment.

# Then do this:
.venv/bin/pip install --upgrade setuptools
```