#!/usr/bin/env python3

import sys
import os, os.path

from jinja2 import Environment, FileSystemLoader, select_autoescape

destdir = 'htdocs'

jenv = Environment(
    loader = FileSystemLoader('templates'),
    extensions = [
    ],
    autoescape = select_autoescape(),
    keep_trailing_newline = True,
)

template = jenv.get_template('front.html')
fl = open(os.path.join(destdir, 'index.html'), 'w')
fl.write(template.render())
fl.close()

template = jenv.get_template('about.html')
fl = open(os.path.join(destdir, 'about/index.html'), 'w')
fl.write(template.render())
fl.close()

