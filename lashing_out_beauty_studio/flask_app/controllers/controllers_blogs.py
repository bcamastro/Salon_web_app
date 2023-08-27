from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.models_users import User
from flask_app.models.models_blog import Blog

@app.route('/blog')
def show_blog():
    if 'user_id' not in session:
        flash("Must be logged in to view blog page")
        return redirect('/login_sign_up')
    data = {
        'id' : session['user_id']
    }
    blog = Blog.get_posts_with_users()
    return render_template('blog.html',user = User.get_by_id(data), blog = blog)

@app.route("/blog_post", methods = ["POST"])
def create_new_post():
    data = {
        "title" : request.form['title'],
        'post_text': request.form['post_text'],
        'user_id': session['user_id']
    }
    Blog.create_post(data)
    return redirect("/blog")

@app.route("/edit/<int:post_id>")
def edit(post_id):
    if 'user_id' not in session:
        return redirect("/logout")
    data = {
        'id' : post_id
    }
    post = Blog.get_one_post(data)
    return render_template("edit.html", post = post)

@app.route("/update/<int:post_id>", methods =["POST"])
def update_post(post_id):
    Blog.update(request.form,post_id)
    return redirect('/blog')

@app.route("/delete/<int:post_id>")
def delete(post_id):
    Blog.delete(post_id)
    return redirect('/blog')