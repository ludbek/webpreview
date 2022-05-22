# web2preview

For a given URL `web2preview` extracts its **title**, **description**, and **image url** using
[Open Graph](http://ogp.me/), [Twitter Card](https://dev.twitter.com/cards/overview), or
[Schema](http://schema.org/) meta tags, or, as an alternative, parses it as a generic webpage.

This is a **fork** of an excellent [webpreview] library and it maintains **complete and absolute**
compatibility with the original while fixing several bugs, enhancing parsing, and adding a new
convenient APIs.

*Main differences between `web2preview` and `webpreview`*:

* Enhanced parsing for generic web pages
* No unnecessary `GET` request is ever made if `content` of the page is supplied
* Complete fallback mechanism which continues to parse until all methods are exhausted
* Python Typings are added across the entire library (**better syntax highlighting**)
* New dict-like `WebPreview` result object makes it easier to read parsing results
* Command-line utility to extract title, description, and image from URL

## Installation

```shell
pip install web2preview
```

## Usage

Use the generic `web2preview` method to parse the page independent of its nature.
It tries to extract the values from Open Graph properties, then it falls back to
Twitter Card format, then Schema. If none of them can extract all three of the title,
description, and preview image, then webpage's content is parsed using a generic
extractor.

```python
>>> from web2preview import web2preview

>>> p = web2preview("https://en.wikipedia.org/wiki/Enrico_Fermi")
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

# This function call won't make any external calls,
# only relying on the supplied content, unlike the example above
>>> web2preview("aa.com", content=content)
WebPreview(url="http://aa.com", title="The Dormouse's story", description="A Mad Tea-Party story")
```

### Using the command line

When `web2preview` is installed via `pip` the accompanying command-line tool is intalled alongside.

```shell
$ web2preview https://en.wikipedia.org/wiki/Enrico_Fermi
title: Enrico Fermi - Wikipedia
description: Italian-American physicist (1901–1954)
image: https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg

$ web2preview https://github.com/ --absolute-url
title: GitHub: Where the world builds software
description: GitHub is where over 83 million developers shape the future of software, together.
image: https://github.githubassets.com/images/modules/site/social-cards/github-social.png
```

*Note*: For the Original [webpreview] API please check the [official docs][webpreview].

## Run with Docker

The docker image can be built and ran similarly to the command line.
The default entry point is the `web2preview` command-line function.

```shell
$ docker build -t web2preview .
$ docker run -it --rm web2preview "https://en.m.wikipedia.org/wiki/Enrico_Fermi"
title: Enrico Fermi - Wikipedia
description: Enrico Fermi (Italian: [enˈriːko ˈfermi]; 29 September 1901 – 28 November 1954) was an Italian (later naturalized American) physicist and the creator of the world's first nuclear reactor, the Chicago Pile-1. He has been called the "architect of the nuclear age"[1] and the "architect of the atomic bomb".
image: https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Enrico_Fermi_1943-49.jpg/1200px-Enrico_Fermi_1943-49.jpg
```

*Note*: built docker image weighs around 210MB.

[webpreview]: https://github.com/ludbek/webpreview