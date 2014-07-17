================
Rate and comment
================

A set of views, forms, widgets and templatetags to use `django-ratings <https://github.com/dcramer/django-ratings>`_
with support of comments and rendering score widgets as stars using `jQuery rating plugin <http://www.fyneworks.com/jquery/star-rating/>`_

Install
=======

from source::

    pip install https://github.com/geelweb/django-ratings/archive/master.zip

Dependances
===========

* django-ratings
* jQuery

Configuring
===========

Add ``geelweb.django.ratings`` to ``INSTALLED_APPS``

Update your db with ``python manage.py syncdb`` or ``python manage.py migrate
newsletters`` if you use `south <http://south.aeracode.org/>`_

Configure django-ratings for your model::

    class Stuff(models.Model):
        rating = RatingField(range=4, can_change_vote=True)

check django-ratings doc for details

Update the urls.py to add the view::

    from geelweb.django.ratings.views import RateView

and add the url::

    url(r'^stuff/(?P<object_id>\d+)/rate/$', login_required(RateView.as_view(app_label='myapp', model='stuff')), name='rate_stuff'),

jQuery rating config
====================

Add jQuery Rating plugin js and css::

    <link href="{% static "star-rating/jquery.rating.css" %}" rel="stylesheet">
    <script src="{% static "star-rating/jquery.rating.pack.js" %}"></script>

Template tags
=============

Load the tags adding ``{% load gw_ratings %}`` to your template

score
-----

Display the score of an instance::

    {% url "rate_stuff" stuff.pk as rate_url %}
    {% score for stuff rate_url %}

comments
--------

Display the comments for an instance::

    {% comments for stuff %}

Display the comments of a user::

    {% comments by user %}
    {% comments for stuff by user %}
