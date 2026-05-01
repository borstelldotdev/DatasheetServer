import json
import os
import requests
from flask import Flask, url_for, render_template, request, redirect, abort
from logging import INFO, DEBUG
import webbrowser

# ladda config
with open("config.json", "r") as config_file:
    config = json.load(config_file)
search_paths: list[str] = config["searchPaths"]
extensions: list[str] = config["extensions"]

if not "documents" in os.listdir("./static"):
    print("Creating static directory...")
    os.mkdir("static/documents")

local_documents = [".".join(x.split(".")[:-1]) for x in os.listdir("static/documents")]

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", local_documents=local_documents)

@app.route("/search/")
def search():
    global local_documents

    query = request.args.get("query")
    if query is None:
        return abort(400)

    name = None
    if query in local_documents:
        static = os.listdir("static/documents")

        for extension in extensions:
            if query + extension in static:
                name = query + extension

    else:
        for search_path in search_paths:
            url = search_path.format(name=query, name_lowercase=query.lower(), name_uppercase=query.upper())
            try:
                response = requests.get(url)
            except requests.exceptions.ConnectionError:
                continue

            if response.status_code == 200:
                name = url.split("/")[-1]
                with open(f"static/documents/{name}", "wb") as file:
                    app.logger.info(f"Downloading {url}...")
                    local_documents.append(query)
                    file.write(response.content)
                    break

    if name is not None:
        return redirect(url_for("static", filename=f"documents/{name}"))

    return redirect(url_for("not_found", query=query))


@app.route("/not_found/")
def not_found():
    return render_template("not_found.html", query=request.args.get("query"))


if __name__ == "__main__":
    app.logger.setLevel(DEBUG if config["debug"] else INFO)
    webbrowser.open(f"http://{config['serverHost']}:{config['serverPort']}")
    app.run(debug=config["debug"], host=config["serverHost"], port=config["serverPort"])
