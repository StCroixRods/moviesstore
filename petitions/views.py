from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition
from django.db.models import Count

@login_required
def index(request):
    petitions = Petition.objects.annotate(num_votes=Count('votes')).order_by('-num_votes')
    template_data = {
        'title': 'Petitions',
        'petitions': petitions
    }
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        if movie_name:
            Petition.objects.create(movie_name=movie_name, user=request.user)
        return redirect('petitions.index')
    template_data = {'title': 'Create Petition'}
    return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
def vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    if request.user != petition.user:
        if request.user in petition.votes.all():
            petition.votes.remove(request.user)
        else:
            petition.votes.add(request.user)
    return redirect('petitions.index')

@login_required
def delete(request, id):
    petition = get_object_or_404(Petition, id=id)
    if request.user == petition.user:
        petition.delete()
    return redirect('petitions.index')