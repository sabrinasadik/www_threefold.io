from jumpscale import j
from flask import render_template, redirect, request
from blueprints.threefoldtoken import blueprint, name

j.tools.markdowndocs.load(
    "https://github.com/threefoldtech/jumpscale_weblibs/tree/master/docsites_examples/threefold",
    name="threefold")
ds = j.tools.markdowndocs.docsite_get("threefold")


@blueprint.route('/')
def route_default():
    return redirect('%s/index.html' % name)


@blueprint.route('/<page>.html')
def route_page(page):
    doc = ds.doc_get(page)
    return render_template('{name}/{page}.html'.format(name=name, page=page), doc=doc)
