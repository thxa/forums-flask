from flask import render_template, request, redirect, url_for, abort, jsonify
from app import models
from app import app, member_store, post_store


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", posts=post_store.get_all())


@app.route("/topic/add", methods=["GET", "POST"])
def topic_add():
    if request.method == "POST":
        post = models.Post(request.form["title"], request.form["content"])
        post_store.add(post)
        return redirect(url_for("home"))
    else:
        return render_template("topic_add.html")


@app.route("/topic/delete/<int:id>")
def topic_delete(id):
    post_store.delete(id)
    return redirect(url_for("home"))


@app.route("/topic/update/<int:id>", methods=["GET", "POST"])
def topic_edit(id):
    post = post_store.get_by_id(id)
    if post is None:
        abort(404)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        post_store.update(post)
        return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("topic_edit.html", post=post)


@app.route("/topic/show/<int:id>", methods=["GET"])
def topic_show(id):
    post = post_store.get_by_id(id)
    if post is None:
        abort(404)
    return render_template("topic_show.html", post=post)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# api
@app.route("/api/topic/all")
def api_topic_get_all():
    posts = [post.__dict__() for post in post_store.get_all()]
    return jsonify(posts)


@app.route("/api/topic/add", methods=["POST"])
def api_topic_create():
    request_data = request.get_json()
    new_post = models.Post(request_data["title"], request_data["content"])
    post_store.add(new_post)
    return jsonify(new_post.__dict__())


@app.route("/api/topic/show/<int:id>", methods=["GET"])
def api_topic_show(id):
    post = post_store.get_by_id(id)
    if post is None:
        abort(404)
    return jsonify(post.__dict__())


@app.route("/api/topic/delete/<int:id>")
def api_topic_delete(id):
    post_store.delete(id)
    return redirect(url_for("api_topic_get_all"))
