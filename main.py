from flask import Flask, redirect, url_for
from flask import request
from flask import render_template
from blog.forms import BlogEntryForm
from blog.models import BlogEntry
from blog import utils
from settings import *
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from google.appengine.api import users

app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True
app.secret_key = "salmanwahed"
pagedown = PageDown(app)
Markdown(app)


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    blog_query = BlogEntry.query(ancestor=utils.get_parent_key())
    bolgs = blog_query.fetch(5)
    return render_template('index.html', blogs=bolgs)


@app.route('/salman/')
def admin():
    blog_query = BlogEntry.query(ancestor=utils.get_parent_key())
    blogs = blog_query.fetch()
    return render_template('admin.html', blogs=blogs)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/blog/')
def blog():
    return render_template('full-width.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/post/<string:blog_id>/<string:slug>/')
@app.route('/post/<string:blog_id>/')
@app.route('/post/preview/<string:blog_id>')
def single_page(blog_id, slug=None):
    blog = BlogEntry.get_by_id(int(blog_id), parent=utils.get_parent_key())
    return render_template('single.html', blog=blog)


@app.route('/new_post/', methods=['GET', 'POST'])
def new_post():
    form = BlogEntryForm(request.form)
    if request.method == 'POST' and form.validate():
        blog_entry = BlogEntry(parent=utils.get_parent_key())
        blog_entry.title = form.title.data
        blog_entry.body = form.body.data
        tag_str = form.tags.data
        blog_entry.tags = map(lambda x: x.strip(), tag_str.split(','))
        blog_entry.save()
        return redirect(url_for('index'))

    return render_template('new_post.html', form=form)


@app.route('/post/update/<string:blog_id>', methods=['GET', 'POST'])
def update_post(blog_id):
    blog = BlogEntry.get_by_id(int(blog_id), parent=utils.get_parent_key())
    return render_template('single.html', blog=blog)


@app.route('/post/delete/<string:blog_id>', methods=['GET', 'DELETE'])
def delete_post(blog_id):
    blog = BlogEntry.get_by_id(int(blog_id), parent=utils.get_parent_key())
    return render_template('single.html', blog=blog)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
