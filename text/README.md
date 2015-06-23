Thesis Management System for Industrial Partner Red Hat
===========

How to build the thesis text
----------------------------

All you need to do is run this command:

    $ make

If you also want to run evince, use this command:

    $ make start

If you want to slice the output pdf file in colered and black pages (using pdftk),
use this command:

    $ make slice

You can also prepend parameter `OD=true` to include the official description of 
the thesis, like this:

    $ make OD=true

