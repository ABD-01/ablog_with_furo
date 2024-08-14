import re
from pathlib import Path

from packaging.version import parse as _parse
from sphinx import addnodes

import ablog

ablog_builder = "dirhtml"
ablog_website = "_website"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx.ext.extlinks",
    "sphinx_automodapi.automodapi",
    "ablog",
    "alabaster",
    "nbsphinx",
    "myst_parser",
]

version = str(_parse(ablog.__version__))
project = "ABlog"
copyright = "2014-2022, ABlog Team"
master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
exclude_patterns = ["_build", "docs/manual/.ipynb_checkpoints"]
html_title = "ABlog"
html_use_index = True
html_domain_indices = False
html_show_sourcelink = True
html_favicon = "_static/ablog.ico"
blog_title = "ABlog"
blog_baseurl = "https://ablog.readthedocs.io/"
blog_locations = {
    "Pittsburgh": ("Pittsburgh, PA", "https://en.wikipedia.org/wiki/Pittsburgh"),
    "San Fran": ("San Francisco, CA", "https://en.wikipedia.org/wiki/San_Francisco"),
    "Denizli": ("Denizli, Turkey", "https://en.wikipedia.org/wiki/Denizli"),
}
blog_languages = {
    "en": ("English", None),
    "nl": ("Nederlands", None),
    "zh_CN": ("Chinese", None),
}
blog_default_language = "en"
language = "en"
blog_authors = {
    "Ahmet": ("Ahmet Bakan", "https://ahmetbakan.com"),
    "Luc": ("Luc Saffre", "https://saffre-rumma.net/luc/"),
    "Mehmet": ("Mehmet Gerçeker", "https://github.com/mehmetg"),
}
blog_feed_archives = True
blog_feed_fulltext = True
blog_feed_templates = {
    "atom": {
        "content": "{{ title }}{% for tag in post.tags %}" " #{{ tag.name|trim()|replace(' ', '') }}" "{% endfor %}",
    },
    "social": {
        "content": "{{ title }}{% for tag in post.tags %}" " #{{ tag.name|trim()|replace(' ', '') }}" "{% endfor %}",
    },
}
disqus_shortname = "https-ablog-readthedocs-io"
disqus_pages = True
fontawesome_link_cdn = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    'custom.css',
]
html_sidebars = {
    "**": [
        # "about.html",
        "furo/sidebar/brand.html",
        "furo/sidebar/search.html",
        "furo/sidebar/scroll-start.html",
        "furo/sidebar/navigation.html",
        "furo/sidebar/rtd-versions.html",

        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/archives.html",
        "ablog/authors.html",
        "ablog/languages.html",
        "ablog/locations.html",
        # "searchbox.html",

        "furo/sidebar/ethical-ads.html",
        "furo/sidebar/scroll-end.html",
        "furo/sidebar/variant-selector.html",
    ]
}
html_theme_options = {
    "light_logo": "ablog-furo.png",
    "dark_logo": "ablog-furo-inverted.png",
    "light_css_variables" : {"color-brand-visited": "var(--color-brand-primary);"},
    "dark_css_variables" : {"color-brand-visited": "var(--color-brand-primary);"},
}
html_title = "ABlog for blogging with Sphinx"
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
extlinks = {
    "wiki": ("https://en.wikipedia.org/wiki/%s", "%s"),
    "issue": ("https://github.com/sunpy/ablog/issues/%s", "issue %s"),
    "pull": ("https://github.com/sunpy/ablog/pull/%s", "pull request %s"),
}
rst_epilog = """
.. _Sphinx: http://sphinx-doc.org/
.. _Python: https://python.org
.. _Disqus: https://disqus.com/
.. _GitHub: https://github.com/sunpy/ablog
.. _PyPI: https://pypi.python.org/pypi/ablog
.. _Read The Docs: https://readthedocs.org/
.. _Alabaster: https://github.com/bitprophet/alabaster
"""
locale_dirs = [str(Path(ablog.__file__).parent / Path("locales"))]
nitpicky = True
nitpick_ignore = []
for line in open("nitpick-exceptions"):
    if line.strip() == "" or line.startswith("#"):
        continue
    dtype, target = line.split(None, 1)
    target = target.strip()
    nitpick_ignore.append((dtype, target))


def parse_event(env, sig, signode):
    event_sig_re = re.compile(r"([a-zA-Z-]+)\s*\((.*)\)")
    m = event_sig_re.match(sig)
    if not m:
        signode += addnodes.desc_name(sig, sig)
        return sig
    name, args = m.groups()
    signode += addnodes.desc_name(name, name)
    plist = addnodes.desc_parameterlist()
    for arg in args.split(","):
        arg = arg.strip()
        plist += addnodes.desc_parameter(arg, arg)
    signode += plist
    return name

def add_marker_js(app):
    app.add_js_file(
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js",
        integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==",
        crossorigin="anonymous",
        referrerpolicy="no-referrer",)
    app.add_js_file("marker.js")

def setup(app):
    from sphinx.ext.autodoc import cut_lines
    from sphinx.util.docfields import GroupedField

    app.connect("autodoc-process-docstring", cut_lines(4, what=["module"]))
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
    app.connect("builder-inited", add_marker_js)
    fdesc = GroupedField("parameter", label="Parameters", names=["param"], can_collapse=True)
    app.add_object_type("event", "event", "pair: %s; event", parse_event, doc_field_types=[fdesc])
