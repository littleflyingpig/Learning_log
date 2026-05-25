from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, Http404
from django.contrib.auth.decorators import login_required
from .models import Topic,Entry
from .form import FormTopic, FormEntry

# Create your views here.
def index(request):
    """编写主页的视图函数"""
    return render(request, 'learning_logs/index.html')

@ login_required
def topic(request):
    """编写主题的视图"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@ login_required
def entry(request, topic_id):
    """编写条目视图"""
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'topic_id':topic_id}
    return render(request, 'learning_logs/entries.html', context)

@ login_required
def new_topic(request):
    """编写添加新主题的视图"""
    if request.method != 'POST':
        form = FormTopic()
    else:
        form = FormTopic(data=request.POST)
        if form.is_valid():

            #form.instance.owner = request.user
            #form.save()
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@ login_required
def new_entry(request, topic_id):
    """编写能添加条目的视图函数"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = FormEntry()
    else: 
        form = FormEntry(data=request.POST)
        if form.is_valid():
            form.instance.topic = topic
            form.save()
            return redirect('learning_logs:entries', topic_id=topic_id)
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

@ login_required
def edit_entry(request, entry_id):
    """编写修改条目的视图函数"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = FormEntry(instance=entry)
    else:
        form = FormEntry(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:entries', topic_id= topic.id)
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }
    return render(request, 'learning_logs/edit_entry.html', context)

@ login_required
def delete_topic(request, topic_id):
    """编写删除主题的视图函数"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    else:
        topic.delete()
        return redirect('learning_logs:topics')
    
@ login_required
def delete_entry(request, entry_id):
    """编写删除条目的视图函数"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    else:
        entry.delete()
        return redirect('learning_logs:entries', topic_id=topic.id)
        