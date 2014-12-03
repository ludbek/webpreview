# About
Webpreview helps preview a webpage. It extracts [Open Graph](http://ogp.me/), [Twitter Card](https://dev.twitter.com/cards/overview) and [Schema](http://schema.org/) meta tags. Given a URL of a page, it extracts title, thumbnail, description, etc as per request.

#Installation

    $ pip install webpreview

#Usage
## Preview a Web Page
Use `web_preview` for extracting title, description and thumbnail image. It tries to extract them from Open Graph properties, if not found it falls back to Twitter Card, and so on  till Schema.  If non works it tries to extract from the webpage's content.

    $ from webpreview import web_preview
    $ title, description, image = web_preview("aurl.com")

## Open Graph
`OpenGraph` extracts Open Graph meta properties. Consider following meta tags.

    <!--doc snippet at aurl.com -->
    <meta property="og:title" content="a title" />
    <meta property="og:description" content="a description" />
    <meta property="article:published_time" content="2013-09-17T05:59:00+01:00" />
    <meta property="og:price:amount" content="15.00" />

Below is a snippet showing its usage.

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

## Twitter Card
`TwitterCard` extracts Twitter Card meta properties from the given webpage. Its usage is similar to `OpenGraph`.

    $ from webpreview import TwitterCard
    $ tc = TwitterCard("aurl.com", ["twitter:title", "twitter:image"])
    $ tc.title
    $ tc.image

## Schema
Webpreview supports Schema through the class `Schema`. Right now it extracts properties in meta tags only.

    $ from webpreview import Schema
    $ aschema = Schema("aurl.com", ["name", "camelCaseProperty"]
    $ aschema.name
    # It makes Camel Case properties available as Snake Case.
    $ aschema.camel_case_property


