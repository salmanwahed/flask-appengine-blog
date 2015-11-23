# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class BlogEntry(ndb.Model):
    title = ndb.StringProperty(verbose_name='title')
    body = ndb.TextProperty(verbose_name='body')
    tags = ndb.StringProperty(verbose_name='tags', repeated=True)
    published = ndb.BooleanProperty(default=False)
    pub_date = ndb.DateProperty(verbose_name='published_on', auto_now=True)
    slug = ndb.StringProperty(verbose_name='slug')

    def save(self):
        self.published = True
        self.slug = '-'.join(self.title.split())
        self.put()

    @property
    def blog_id(self):
        return str(self.key.id())

    @property
    def absolute_url(self):
        return 'post' + '/' + self.blog_id + '/' + self.slug

    def __repr__(self):
        return "<Blog: %r>" % self.title
