# Introduction

In this repository, I collect some (embarrassingly simplistic) tools I use to make my [OCR4all](https://github.com/OCR4all) workflow a bit more efficient.

# PageXML Editor

Jupyter notebook to speed up targeted GT generation. Selects lines that match a certain regex pattern for correction/transcription.

# Best practices

Some regex that have proved useful for my (early modern, Latin) use cases:

* `(fſ|ſf)`
* `[qQ][^u]`
* `(.)\1{3,}`

# Models

The `models` directory contains some `calamari` models.

## Cyrillic

The `cyrillic` model was trained on 64k lines of synthetically created GT, using about 8 different fonts. Its performance on historical prints is still very poor, but maybe it can serve as a point of departure.
