#!/usr/bin/env python3
"""Assembles index.html from template.html + content.json + images.json + images/.

Run from this directory: python3 build.py
"""
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    template = read(os.path.join(HERE, "template.html"))
    content = read(os.path.join(HERE, "content.json"))
    images_meta = read(os.path.join(HERE, "images.json"))
    font_faces = read(os.path.join(HERE, "fonts", "notokr-fontfaces.css"))

    images_meta_list = json.loads(images_meta)
    images_data = {}
    for im in images_meta_list:
        path = os.path.join(HERE, "images", im["file"].replace(".png", ".jpg"))
        with open(path, "rb") as f:
            images_data[im["file"]] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")

    out = template
    out = out.replace("/*__FONT_FACES__*/", font_faces)
    out = out.replace("/*__CONTENT_JSON__*/", content)
    out = out.replace("/*__IMAGES_META__*/", images_meta)
    out = out.replace("/*__IMAGES_DATA__*/", json.dumps(images_data, ensure_ascii=False))

    out_path = os.path.join(HERE, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"wrote {out_path} ({os.path.getsize(out_path) / 1024 / 1024:.2f} MB)")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    main()
