# web2preview

For a given URL `web2preview` extracts its **title**, **description**, and **image url** using
[Open Graph](http://ogp.me/), [Twitter Card](https://dev.twitter.com/cards/overview), or
[Schema](http://schema.org/) meta tags, or, as an alternative, parses it as a generic webpage.

## Installation

```shell
pip install web2preview
```

## Usage

The library retrieves the contents of webpage by making a `GET` request using `requests` library.

There are two main helper functions that can be used to do that `webpreview` and `web_preview`.


### Generic WebPage Preview

Use `web_preview` for extracting title, description and thumbnail image. It tries to extract them from Open Graph properties, if not found it falls back to Twitter Card, and so on  till Schema.  If non works it tries to extract from the webpage's content.

```python
from web2preview import web_preview
title, description, image = web_preview("aurl.com")

# specifing timeout or headers which gets passed to requests.get()
headers = {'User-Agent': 'Mozilla/5.0'}
title, description, image = web_preview("a_slow_url.com", timeout=1000, headers=headers)

# pass html content thus avoiding making http call again to fetch content.
content = """<html><head><title>Dummy HTML</title></head></html>"""
title, description, image = web_preview("aurl.com", content=content)

# specifing the parser
# by default webpreview uses 'html.parser'
title, description, image = web_preview("aurl.com", content=content, parser='lxml')
```

### Open Graph

`OpenGraph` extracts Open Graph meta properties. Consider following meta tags.

```html
<!--doc snippet at aurl.com -->
<meta property="og:title" content="a title" />
<meta property="og:description" content="a description" />
<meta property="article:published_time" content="2013-09-17T05:59:00+01:00" />
<meta property="og:price:amount" content="15.00" />
```

Below is a snippet showing its usage.

```python
$ from webpreview import OpenGraph

# pass a URL and a list of meta properties
$ og = OpenGraph("http://aurl.com", ["og:title", "article:published_time", "og:price:amount"])

# OpenGraph dynamically assigns corresponding properties to its instance. As you will see it excludes `og:` from the supplied properties.
$ og.title
=> "a title"
$ og.published_time
=> "2013-09-17T05:59:00+01:00"

# It converts `:` in a property into `_`.
$ og.price_amount
=> "15.00"
```

### Twitter Card

`TwitterCard` extracts Twitter Card meta properties from the given webpage. Its usage is similar to `OpenGraph`.

```python
$ from webpreview import TwitterCard
$ tc = TwitterCard("aurl.com", ["twitter:title", "twitter:image"])
$ tc.title
$ tc.image
```

### Schema

Webpreview supports Schema through the class `Schema`. Right now it extracts properties in meta tags only.

```python
$ from webpreview import Schema
$ aschema = Schema("aurl.com", ["name", "camelCaseProperty"]
$ aschema.name
# It makes Camel Case properties available as Snake Case.
$ aschema.camel_case_property
```

## Run with Docker

```shell
docker build -t web2preview .
docker run -it --rm web2preview "https://en.m.wikipedia.org/wiki/Enrico_Fermi"
```

### Run your script

    $ docker run -it --rm --name my-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp webpreview python your-script.py
