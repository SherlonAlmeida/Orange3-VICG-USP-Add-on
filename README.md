Orange3 VICG-USP Add-on
======================

This is an add-on for [Orange3](http://orange.biolab.si).
In this add-on you will find a widget of [Least Square Projection (LSP)](https://dl.acm.org/citation.cfm?id=1399373).
The code inside the widget is from the [mppy](https://pypi.org/project/mppy/) library, implemented by [Thiago Henrique](https://github.com/thiagohenriquef/mppy).

Installation
------------

To install the add-on, run

    pip install .

To register this add-on with Orange, but keep the code in the development directory (do not copy it to 
Python's site-packages directory), run

    pip install -e .

Usage
-----

After the installation, the widget from this add-on is registered with Orange. To run Orange from the terminal,
use

    python -m Orange.canvas

The new widget appears in the toolbox bar.
In the Workflows directory there are some examples.

![screenshot](https://github.com/SherlonAlmeida/Orange3-VICG-USP-Add-on/blob/master/screenshot.png)