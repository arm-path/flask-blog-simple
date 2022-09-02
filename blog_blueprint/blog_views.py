from slugify import slugify
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_security import login_required

from models import db, Post, Tag
from .blog_forms import PostForm, TagForm

blog = Blueprint('blog_blueprint', __name__, template_folder='templates')


@blog.route('/')
def post_list():
    title = "Список постов"
    search = request.args.get('search')
    page = int(request.args.get('page')) if request.args.get('page') and request.args.get('page').isdigit() else 1
    posts = Post.query.filter(Post.title.contains(search) | Post.content.contains(search)) if search else Post.query
    pages = posts.paginate(page=page, per_page=3)
    return render_template('blog_templates/post_list.html', title=title, posts=posts, pages=pages)


@blog.route('/post/<slug>/')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('blog_templates/post_detail.html', post=post)


@blog.route('/tag/<slug>/posts/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    title = f"Посты по тегу: {tag.title}"
    posts = tag.posts
    page = int(request.args.get('page')) if request.args.get('page') and request.args.get('page').isdigit() else 1
    pages = posts.paginate(page=page, per_page=3)
    return render_template('blog_templates/post_list.html', title=title, posts=posts, pages=pages, tag=tag)


def post_create_or_update(request_data):
    tag_list = [int(id_number) for id_number in request_data.getlist('tags') if id_number.isdigit()]
    tags = Tag.query.filter(Tag.id.in_(tag_list)).all()
    title = request_data['title']
    content = request_data['content']
    return {'title': title, 'content': content, 'tags': tags}


@blog.route('/create/post/', methods=["POST", "GET"])
@login_required
def post_create():
    title = "Создание поста"
    action = "Добавить"
    form = PostForm()
    if request.method == "POST":
        post_data = post_create_or_update(request.form)
        if post_data['title'] and post_data['content']:
            post = Post(title=post_data['title'], content=post_data['content'])
            for tag in post_data['tags']:
                post.tags.append(tag)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog_blueprint.post_detail', slug=post.slug))
    return render_template('blog_templates/post_create_or_update.html', title=title, action=action, form=form)


@blog.route('/update/post/<slug>/', methods=["POST", "GET"])
@login_required
def post_update(slug):
    title = "Редактирование поста"
    action = "Обновить"

    post = Post.query.filter(Post.slug == slug).first_or_404()
    form = PostForm(obj=post)

    if request.method == "POST":
        post_data = post_create_or_update(request.form)
        if post_data['title'] and post_data['content']:
            slug = slugify(post_data['title'])
            if not Post.query.filter(Post.slug == slug).first() or post.slug == slug:
                post.title = post_data['title']
                post.content = post_data['content']
                post.slug = slug
                post.tags = []
                for tag in post_data['tags']:
                    post.tags.append(tag)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('blog_blueprint.post_detail', slug=post.slug))
    return render_template('blog_templates/post_create_or_update.html', title=title, action=action, form=form)


@blog.route('/create/tag/', methods=["POST", "GET"])
@login_required
def tag_create():
    title = "Добавление тега"
    action = "Добавить"
    form = TagForm()
    if request.method == "POST":
        if request.form['title'] and not Tag.query.filter(Tag.slug == slugify(request.form['title'])).first():
            tag = Tag(title=request.form['title'])
            db.session.add(tag)
            db.session.commit()
            return redirect(url_for('blog_blueprint.post_create'))
    return render_template('blog_templates/tag_create_or_update.html', title=title, action=action, form=form)


@blog.route('/update/tag/<slug>/', methods=["POST", "GET"])
@login_required
def tag_update(slug):
    title = "Редактирование тега"
    action = "Редактировать"
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    if tag:
        form = TagForm(obj=tag)
        if request.method == "POST":
            form = TagForm(formdata=request.form, obj=tag)
            form.populate_obj(tag)
            db.session.commit()
            return redirect(url_for('blog_blueprint.tag_detail', slug=tag.slug))
        return render_template('blog_templates/tag_create_or_update.html', title=title, action=action, form=form)
