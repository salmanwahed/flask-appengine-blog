# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from settings import *


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def get_parent_key(blogentry_name=DEFAULT_BLOGENTRY_NAME):
    """Constructs a Datastore key for a BlogEntry entity.

    We use blogentry_name as the key.
    """
    return ndb.Key('BlogEntry', blogentry_name)
