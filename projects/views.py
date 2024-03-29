from django.shortcuts import render, redirect
from .models import Project,Tag
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import search_projects,paginate_projects


def get_projects(request):
    projects,search_query=search_projects(request)
    projects,custom_range=paginate_projects(request,projects,6)

    context = {
        "projects": projects,
        "search_query":search_query,
        "custom_range":custom_range,
    }
    return render(request, 'projects/projects.html', context)


def get_project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form=ReviewForm()
    if request.method=="POST":
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=project_obj
        review.owner=request.user.profile
        review.save()
        # Updating voting each time reviewed
        project_obj.update_vote
        return redirect('project',pk=project_obj.id)
    return render(request, 'projects/single-project.html', {'project': project_obj,'form':form})


@login_required(login_url='login')
def create_project(request):
    profile=request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        new_tags = request.POST.get('new_tags').replace(",", " ").split()
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method == "POST":
        new_tags = request.POST.get('new_tags').replace(","," ").split()
        form=ProjectForm(request.POST,request.FILES,instance=project)
        project=form.save()
        for tag in new_tags:
            tag,created = Tag.objects.get_or_create(name=tag)
            project.tags.add(tag)
        return redirect('account')

    return render(request,'projects/project_form.html',context={'form':form,'project':project})


@login_required(login_url='login')
def delete_project(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    context={'object':project}
    if request.method=='POST':
        project.delete()
        return redirect('account')

    return render(request,'delete_template.html',context=context)