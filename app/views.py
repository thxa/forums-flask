from flask import render_template, request, redirect, url_for
from app import models
from app import app, member_store, post_store


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", posts=post_store.get_all())


@app.route("/topic/add", methods=["GET", "POST"])
def topic_add():
    if request.method == "POST":
        new_post = models.Post(request.form["title"], request.form["content"])
        post_store.add(new_post)
        return redirect(url_for("home"))
    else:
        return render_template("topic_add.html")


@app.route("/topic/delete/<int:_id>")
def topic_delete(_id):
    post_store.delete(_id)
    return redirect(url_for("home"))


@app.route("/topic/update/<int:_id>", methods=["GET", "POST"])
def topic_edit(_id):
    if request.method == "POST":
        edit_post = post_store.get_by_id(_id)
        edit_post.title = request.form["title"]
        edit_post.content = request.form["content"]
        post_store.update(edit_post)
        return redirect(url_for("home"))
    else:
        edit_post = post_store.get_by_id(_id)
        return render_template("topic_edit.html", post=edit_post)


@app.route("/topic/show/<int:_id>", methods=["GET"])
def topic_show(_id):
    post_show = post_store.get_by_id(_id)
    return render_template("topic_show.html", post=post_show)
