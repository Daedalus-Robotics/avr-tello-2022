import json
from guizero import Picture, App


def turn_off_all_photos(*args):
    for picture in args:
        # print(f"func {picture}")
        picture.visible = False


def setup_field(app: App = None) -> dict:
    links = json.load(open("assets/field.json", "r"))
    field = {}

    for str_id, link in links.items():
        field[int(str_id)] = Picture(app, image=link, align="bottom", visible=False)

    return field
