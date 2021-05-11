# Introduction

In this repository, I collect some (embarrassingly simplistic) tools I use to make my [OCR4all](https://github.com/OCR4all) workflow a bit more efficient.

# PageXML Editor

Jupyter notebook to speed up targeted GT generation. Selects lines that match a certain regex pattern for correction/transcription.

# Best practices

Some regex that have proved useful for my (early modern, Latin) use cases:

* `(fſ|ſf)`
* `[qQ][^u]`
* `(.)\1{3,}`

# Tesseract on PageXML

`tess_page` contains a simple function that applies Tesseract ([`pytesseract`](https://pypi.org/project/pytesseract/)) to PageXML files. Requires a functioning `pytesseract` configuration and `PIL`.

`tess_pagexml` takes the OCR4all project directory (containing the `processing` subfolder with binarized png files and pagexml) as an argument and substitutes existing OCR with tesseract OCR or writes new OCR if there is none.

The original pagexml is stored as a backup in a directory `old_processing`.

The function `mask` could be useful as well: It takes a list of vertices and optionally a named argument (`img` = "string") and returns a line snippet. As a default, it expects that the `img` variable has already been defined.

## Cyrillic

The `cyrillic` model was trained on 64k lines of synthetically created GT, using about 8 different fonts. Its performance on historical prints is still very poor, but maybe it can serve as a point of departure.
