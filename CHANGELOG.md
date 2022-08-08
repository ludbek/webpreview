# Changelog

## [v1.1.3](https://github.com/vduseev/web2preview/tree/v1.1.3) (2022-06-08)

* Added Python 3.7 support and tests
* Sanitize generic title and description from unknown unicode and whitespaces
* Handle URLs with underscode `_` character in the domain name

[Full Changelog](https://github.com/vduseev/web2preview/compare/v1.1.1...v1.1.3)

## [v1.1.1](https://github.com/vduseev/web2preview/tree/v1.1.1) (2022-05-24)

Modern reimplementation of `web_preview`:

* Enhanced parsing for generic web pages
* No unnecessary `GET` request is ever made if `content` of the page is supplied
* Complete fallback mechanism which continues to parse until all methods are exhausted
* Python Typings are added across the entire library (**better syntax highlighting**)
* New dict-like `WebPreview` result object makes it easier to read parsing results
* Command-line utility to extract title, description, and image from URL

[Full Changelog](https://github.com/vduseev/web2preview/compare/1.6.0...v1.1.1)
