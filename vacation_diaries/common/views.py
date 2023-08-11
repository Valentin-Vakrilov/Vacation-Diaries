from django.views import generic as views
from vacation_diaries.vacations.models import Vacation
from .forms import SearchForm
from vacation_diaries.photos.models import Comment, Like


class IndexView(views.ListView):
    template_name = "common/index.html"
    model = Vacation
    context_object_name = "vacations"
    search_form = SearchForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        vacation_main_photos = []
        vacation_details = []

        searched_vacation = self.request.GET.get("vacation")

        if searched_vacation:
            context["vacations"] = context["vacations"].filter(destination__icontains=searched_vacation)

        for vacation in context["vacations"]:
            main_photo = vacation.photo_set.first()
            comments = Comment.objects.filter(commented_photo=main_photo)
            total_likes = Like.objects.filter(liked_photo=main_photo).count()

            vacation_main_photos.append(main_photo)

            creator = None

            if main_photo:
                creator = main_photo.user
                context["creator"] = creator

            vacation_details.append({
                "vacation": vacation,
                "main_photo": main_photo,
                "comments": comments,
                "total_likes": total_likes,
                "creator": creator
            })

        context["vacation_details"] = vacation_details

        return context
