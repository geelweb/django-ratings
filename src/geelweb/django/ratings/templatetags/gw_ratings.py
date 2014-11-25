import random
import string

from django import template
from django.contrib.contenttypes.models import ContentType

from geelweb.django.ratings.models import RatingComment

register = template.Library()

class CommentsNode(template.Node):
    DEFAULT_TEMPLATE = 'ratings/comments.html'

    def __init__(self, instance=None, user=None, template_file=None):
        if instance:
            self.instance = template.Variable(instance)
        else:
            self.instance = None

        if user:
            self.user = template.Variable(user)
        else:
            self.user = None

        if template_file:
            self.template = template_file
        else:
            self.template = self.DEFAULT_TEMPLATE

    def render(self, context):
        comments = RatingComment.objects.all()
        if self.instance:
            instance = self.instance.resolve(context)
            content_type = ContentType.objects.get_for_model(instance)
            comments = comments.filter(content_type=content_type, object_id=instance.pk)
        if self.user:
            comments = comments.filter(user=self.user.resolve(context))

        comments = comments.order_by('-date_created')

        t = template.loader.get_template(self.template)
        return t.render(template.Context({'comments': comments}, autoescape=context.autoescape))

class ScoreNode(template.Node):
    DEFAULT_TEMPLATE = 'ratings/score.html'

    def __init__(self, instance=None, template_file=None, vote_url=None):
        self.instance = template.Variable(instance)

        if template_file:
            self.template = template_file
        else:
            self.template = self.DEFAULT_TEMPLATE

        if vote_url:
            self.vote_url = template.Variable(vote_url)
        else:
            self.vote_url = None

    def render(self, context):
        instance = self.instance.resolve(context)
        t = template.loader.get_template(self.template)
        vote_url = None
        if self.vote_url:
            vote_url = self.vote_url.resolve(context)
        return t.render(template.Context({
                'instance': instance,
                'vote_url': self.vote_url.resolve(context) if self.vote_url else None,
                'hash': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            }, autoescape=context.autoescape))

@register.tag
def comments(parser, token):
    """
    Retrieve comments for an instance and/or create by a user and render them
    using a template

    Syntax::

        {% comments [for instance] [by user] [with template] %}

    Examples::

        {% comments for poll %}
        {% comments for poll by request.user %}
        {% comments for poll by request.user with 'myapp/comments.html' %}
    """

    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "[for instance] [by user] [with template]" %
                      dict(tag_name=bits[0]))

    # if there is an odd number of bits, we've got an error
    if len(bits) % 2 == 0:
        raise template.TemplateSyntaxError(syntax_message)

    instance = None
    user = None
    template = None

    for i in [1, 3, 5]:
        if len(bits) <= i:
            break
        k = bits[i]
        if k == 'for':
            instance = bits[i+1]
        elif k == 'by':
            user = bits[i+1]
        elif k == 'with':
            template = bits[i+1]
        else:
            raise template.TemplateSyntaxError(syntax_message)

    return CommentsNode(instance=instance, user=user, template_file=template)

@register.tag
def score(parser, token):
    """
    Display the score of an instance with the number of votes and a link to add
    a comment

    Syntax::

        {% score for instance [with template] [rate_url] %}

    Examples::
        {% score for poll %}
        {% score for poll '/poll/rate/2' %}
        {% score for poll with 'template/score.html' %}
        {% score for poll with 'template/score.html' /poll/rate/2' %}
    """

    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "for instance" %
                      dict(tag_name=bits[0]))

    if len(bits) < 3 or len(bits) > 6:
        raise template.TemplateSyntaxError(syntax_message)

    if bits[1] != 'for':
        raise template.TemplateSyntaxError(syntax_message)
    instance = bits[2]

    # if the number of bits is odd, the last one is the vote url
    vote_url = None
    if len(bits) % 2 == 0:
        vote_url = bits[-1]

    template = None
    if len(bits) > 4:
        if bit[3] != 'with':
            raise template.TemplateSyntaxError(syntax_message)
        template = bits[4]

    return ScoreNode(instance=instance, template_file=template, vote_url=vote_url)
