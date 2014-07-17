from django.forms.util import flatatt

from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from django.forms.widgets import RadioChoiceInput, ChoiceFieldRenderer

class StarRadioChoiceInput(RadioChoiceInput):
    def __init__(self, *args, **kwargs):
        super(StarRadioChoiceInput, self).__init__(*args, **kwargs)

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        return format_html(self.tag())

class StarRadioFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = StarRadioChoiceInput

    def render(self):
        return mark_safe(u'\n%s\n' % u'\n'.join([u'%s' %
            force_unicode(w) for w in self]))


