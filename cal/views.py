from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import JsonResponse
import calendar
from django.contrib.auth.decorators import login_required

from .models import *
from .utils import Calendar
from .forms import EventForm

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required(login_url='authentications/login/')
def event(request, event_id=None):
    # instance = Event()
    # if event_id:
    #     instance = get_object_or_404(Event, pk=event_id)
    # else:
    #     instance = Event()

    # form = EventForm(request.POST or None, instance=instance)
    # if request.POST and form.is_valid():
    #     form.save()
    #     return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html')

def event_post(request):
    print("bbb")
    if request.method == 'POST':
        print("aaa")
        title = request.POST['title']
        description = request.POST['description']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        mood_new = Event(title=title, description=description, start_time=start_time, end_time=end_time)
        mood_new.save()
        mood= {'title': mood_new.title, 'description':mood_new.description, 'start_time':mood_new.start_time,'end_time':mood_new.end_time}
        data={ 
            'mood':mood,
            'url': 'cal/calendar'}
    return JsonResponse(data)