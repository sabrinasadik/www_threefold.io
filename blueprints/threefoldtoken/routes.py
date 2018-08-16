from jumpscale import j
from flask import render_template, redirect
from . import blueprint, name

j.tools.markdowndocs.load(
    "https://github.com/threefoldfoundation/www_threefold.io/tree/digital-me/threefold",
    name="threefold")
ds = j.tools.markdowndocs.docsite_get("threefold")


@blueprint.route('/')
def route_default():
    return redirect('%s/index.html' % name)


@blueprint.route('/<page>.html')
def route_page(page):
    try:
        doc = ds.doc_get(page)
    except:
        doc = None
    return render_template('{name}/{page}.html'.format(name=name, page=page), name=name, doc=doc)
