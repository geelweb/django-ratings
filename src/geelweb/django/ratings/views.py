from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from django.contrib import messages
from geelweb.django.ratings.forms import RatingForm
from geelweb.django.ratings.models import RatingComment

#@login_required
#def rate(request, pk):
#    user = get_object_or_404(User, pk=pk)
#    form = RatingForm(request.POST or None)
#    if form.is_valid():
#        user.userprofile.rating.add(score=form.cleaned_data['rating'], user=request.user, ip_address=request.META['REMOTE_ADDR'])
#
#        comment = RatingComment(user=request.user, grower=user,
#                score=form.cleaned_data['rating'],
#                comment=form.cleaned_data['comment'])
#        comment.save()
#
#        return HttpResponseRedirect(reverse('accounts_grower_detail', kwargs={"pk":pk}))
#
#    return render_to_response('ratings/rate.html', {
#        'user': user,
#        'form': form,
#        }, context_instance=RequestContext(request))

class RateView(View):
    template = 'ratings/rate.html'

    app_label = None
    model = None

    def get(self, request, object_id):
        content_type = self.get_content_type(self.app_label, self.model)
        instance = self.get_instance(content_type.id, object_id)

        initial = {}
        try:
            comment = RatingComment.objects.get(user=request.user,
                    content_type=content_type, object_id=object_id)
            initial['comment'] = comment.comment
        except RatingComment.DoesNotExist:
            pass

        initial['rating'] = instance.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR'])

        form = RatingForm(initial=initial)
        return render_to_response(self.template, {
            'instance': instance,
            'form': form,
            }, context_instance=RequestContext(request))

    def post(self, request, object_id):
        content_type = self.get_content_type(self.app_label, self.model)
        instance = self.get_instance(content_type.id, object_id)
        form = RatingForm(request.POST)
        if form.is_valid():
            instance.rating.add(score=form.cleaned_data['rating'],
                    user=request.user, ip_address=request.META['REMOTE_ADDR'])

            try:
                comment = RatingComment.objects.get(user=request.user,
                        content_type=content_type, object_id=object_id)
                msg = 'Thanks, your comment has been updated'
            except RatingComment.DoesNotExist:
                comment = RatingComment(user=request.user,
                        content_type=content_type, object_id=object_id)
                msg = 'Thanks, your comment has been saved'

            comment.score = form.cleaned_data['rating']
            comment.comment = form.cleaned_data['comment']
            comment.save()

            messages.add_message(request, messages.SUCCESS, msg)

            # TODO the redirect url must be dynamic
            #return HttpResponseRedirect(reverse('accounts_grower_detail', kwargs={"pk":object_id}))

        return render_to_response(self.template, {
            'instance': instance,
            'form': form,
            }, context_instance=RequestContext(request))

    def get_content_type(self, app_label, model):
        try:
            content_type = ContentType.objects.get(model=model,
                    app_label=app_label)
        except ContentType.DoesNotExist:
            raise Http404("Invalid 'model' or 'app_label'")
        return content_type

    def get_instance(self, content_type_id, object_id):
        return ContentType.objects.get(pk=content_type_id).get_object_for_this_type(pk=object_id)

