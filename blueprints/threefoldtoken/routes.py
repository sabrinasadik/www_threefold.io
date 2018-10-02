import os
from PIL import Image
from Jumpscale import j
from flask import render_template, redirect
from . import blueprint, name

j.tools.markdowndocs.load(
    "https://github.com/threefoldfoundation/www_threefold.io/tree/digital-me/threefold",
    name="threefold")
ds = j.tools.markdowndocs.docsite_get("threefold")

team_repo = "ssh://git@docs.grid.tf:7022/%s/data_team.git"


def process_image(img_path, parent_path):
    img = Image.open(img_path)
    if img.height != img.width:
        side = min((img.width, img.height))
        img = img.crop((0, 0, side, side))

    side = 252
    if img.height != side:
        img = img.resize((side, side))
    new_processed_image = "{}/processed.jpg".format(parent_path)
    img.save(new_processed_image)
    return new_processed_image


def process_team():
    target = j.sal.fs.joinPaths(j.sal.fs.getParent(os.path.abspath(__file__)), "static")
    js_target = '{}/js/data.js'.format(target)
    avatars_target = '{}/avatars'.format(target)
    all_files = {}
    companies = ["bettertoken", "threefold"]
    for company in companies:
        company_repo = j.clients.git.getContentPathFromURLorPath(team_repo % "threefold")
        j.sal.fs.changeDir(company_repo)
        j.tools.team_manager.do()
        for department_path in j.sal.fs.listDirsInDir(company_repo + "/team", recursive=False):
            department = j.sal.fs.getBaseName(department_path)
            for person_path in j.sal.fs.listDirsInDir(department_path, recursive=False):
                # Get toml file
                toml_file = "{}/person.toml".format(person_path)
                if not j.sal.fs.exists(toml_file):
                    continue
                all_files[person_path] = {
                    'team': company,
                    'department': department,
                    'toml': toml_file,
                }

                # Get processed image
                unprocessed_image = "{}/unprocessed.jpg".format(person_path)
                processed_image = "{}/processed.jpg".format(person_path)
                if j.sal.fs.exists(processed_image):
                    all_files[person_path]['image'] = processed_image
                elif j.sal.fs.exists(unprocessed_image):
                    all_files[person_path]['image'] = process_image(unprocessed_image, person_path)

    sections = []
    for person_path, files in all_files.items():
        # skip all soft links that their links are already exists
        if j.sal.fs.isLink(person_path) and j.sal.fs.readLink(person_path) in all_files:
            continue
        print("Processing: %s" % person_path)
        try:
            person = j.data.serializers.toml.load(files['toml'])
        except Exception as e:
            print("Error: {}".format(files['toml']))
            continue

        first_name = person.get('first_name', '')
        last_name = person.get('last_name', '')
        name = "{} {}".format(first_name, last_name)
        login = person.get('login')
        description = person.get('description_public_friendly') or \
                      person.get("description_public_formal") or \
                      person.get("description_internal")
        linked_in = person.get('linkedin')
        telegram = person.get('telegram')
        emails = person.get('email')
        hobbies = person.get('hobbies')
        skype = person.get('skype')
        links = person.get('links')
        github = person.get('github')
        core = person.get('core')
        rank = person.get('rank')
        avatar_name = ""
        if files.get('image'):
            avatar_name = "{}_{}".format(j.sal.fs.getBaseName(person_path), j.sal.fs.getBaseName(files['image']))
            j.sal.fs.copyFile(files['image'], "{}/{}".format(avatars_target, avatar_name))
        sections.append({
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "login": login,
            "description": description,
            "linked_in": linked_in,
            "skype": skype,
            "github": github,
            "avatar": avatar_name,
            "telegram": telegram,
            "emails": emails,
            "hobbies": hobbies,
            "links": links,
            "core": core,
            "rank": rank
        })

    # write dict to the javascript file
    data = j.data.serializers.json.dumps(sections)
    j.sal.fs.writeFile(js_target, "var team = {};".format(data))


process_team()


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
