from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


from core.models import Profile

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.views import View

User = get_user_model()

# class UserDisplay(View):

#     def get(self, request):
    
#         available_users = Profile.objects.exclude(user=request.user)
#         context = {
#             'users': available_users
#         }
#         return render(request, "myprofile.html", context)
  

# class FriendRequestView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def send_friend_request(request, id):
#         user = get_object_or_404(User, id=id)
#         frequest, created = FriendRequest.objects.get_or_create(
#             from_user=request.user,
#             to_user=user)
#         return HttpResponseRedirect('/users')

# def cancel_friend_request(request, id):
# 	if request.user.is_authenticated:
# 		user = get_object_or_404(User, id=id)
# 		frequest = FriendRequest.objects.filter(
# 			from_user=request.user,
# 			to_user=user).first()
# 		frequest.delete()
# 		return HttpResponseRedirect('/users')

# def accept_friend_request(request, id):
# 	from_user = get_object_or_404(User, id=id)
# 	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
# 	user1 = frequest.to_user
# 	user2 = from_user
#     # TODO make this non symmetric
# 	user1.profile.friends.add(user2.profile)
# 	user2.profile.friends.add(user1.profile)
# 	frequest.delete()
# 	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

# def delete_friend_request(request, id):
# 	from_user = get_object_or_404(User, id=id)
# 	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
# 	frequest.delete()
# 	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))




from django.views.generic import TemplateView,View
from django.shortcuts import render
from django.shortcuts import get_object_or_404

class ManageFriendsTemplateViewView(TemplateView):
    template_name = 'manage_friends.html'


class ProfileDetailView(View):

    def view_profile(request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        return render(request,'user_profile.html')

