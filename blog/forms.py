# -*- coding: utf-8 -*-

from flask_wtf import Form
from flask_pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class BlogEntryForm(Form):
    title = StringField('title', validators=[DataRequired()])
    body = PageDownField("Enter in markdown syntax")
    tags = StringField('tags', validators=[DataRequired()])
    submit = SubmitField("Publish")

