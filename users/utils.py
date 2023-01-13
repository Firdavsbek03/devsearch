from .models import Profile,Skill
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def paginate_profiles(request,profiles,result_per_page):
    paginator=Paginator(profiles,result_per_page)
    page=request.GET.get('page')
    try:
        profiles=paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        profiles=paginator.page(page)

    left_index=int(page)-1
    if left_index<1:
        left_index=1

    right_index=int(page)+2
    if right_index>paginator.num_pages:
        right_index=paginator.num_pages
    custom_range=(left_index,right_index)

    return profiles,custom_range


def search_profiles(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get("search_query")
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )
    return search_query,profiles
