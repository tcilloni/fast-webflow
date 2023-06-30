# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'fast-webflow'
copyright = '2023, Thomas Cilloni'
author = 'Thomas Cilloni'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']


###################################################################################################
###################################################################################################

# https://github.com/coderefinery/documentation-example/blob/main/doc/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../fast_webflow'))

master_doc = 'index'
extensions = ['sphinx.ext.autodoc', 'myst_parser']
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_static_path = []

# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}