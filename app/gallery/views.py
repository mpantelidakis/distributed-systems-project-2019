from django.views.generic import TemplateView,View
from django.http import HttpResponseNotFound
from core.models import Gallery
from django.shortcuts import render
from django.shortcuts import get_object_or_404


class GalleryListTemplateView(TemplateView):
    template_name = 'gallery_list.html'

class GallreyDetailView(View):

    def view_gallery(request, pk):
        gallery = get_object_or_404(Gallery, id=pk)
        return render(request,'gallery_detail.html')

    