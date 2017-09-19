from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import TemplateView
# Import necessary classes
from django.http import HttpResponse
from myapp.models import Author, Book, Course,Student,Topic
from myapp.forms import TopicForm,InterestForm,RegistrationForm
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
# Create your views here.
#def index(request):
#    courselist = Course.objects.all() [:10]
#    authorlist = Author.objects.all().order_by('birthdate')
#    response = HttpResponse()
#    heading1 = '<p>' + 'List of courses: ' + '</p>'
#   response.write(heading1)
#   for course in courselist:
#      para = '<p>' + str(course) + '</p>'
#     response.write(para)
#    heading2 = '<p>' + 'List of Authors: ' + '</p>'
#    response.write(heading2)
#    for author in authorlist:
#        para = '<p>' + str(author) + '</p>'
#        response.write(para)
#    return response
#def index(request):
#    courselist = Course.objects.all().order_by('title')[:10]
#    return render(request, 'myapp/index.html', {'courselist': courselist})
class index(TemplateView):
 #   courselist = Course.objects.all().order_by('title')[:10]

  template_name = 'myapp/index.html'
  def courselist(self):
    return (Course.objects.all().order_by('title')[:10])



#def about(request):
 #    response = HttpResponse()
 #    heading1 = '<p>' + 'This is a Course Listing APP' + '<p>'
 #    response.write(heading1)
 #    return response
#def about(request):
#    if not request.user.is_authenticated():
#        return redirect(reverse('myapp:index'))
#    else:
#     return render(request, 'myapp/about0.html')
class about(TemplateView):
    template_name = "myapp/about0.html"
#def detail(request,course_no):
#     courselist = Course.objects.all()
#     courselist = get_object_or_404(Course, pk = course_no)
#     response = HttpResponse()
#     heading1 = '<p>' + 'Title' + ':' + str(courselist.title) + '<br>' + 'Course Number' + ':' + str(courselist.course_no) + '<br>' + 'Textbook' + ':' + str(courselist.textbook) + '<p>'
#    response.write(heading1)
#     return response

def detail(request,course_no):

    course_no = get_object_or_404(Course, pk=course_no)

    return render(request, 'myapp/detail0.html', {'course': course_no})
def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topics.html',{'topiclist':   topiclist})
def addtopic(request):
 #  return HttpResponse('You can add new topic here')
    topiclist = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses = 1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
        else:
            return render(request, 'myapp/topics.html', {'form':form, 'topiclist':topiclist})
    else:
        form = TopicForm()
    return render(request, 'myapp/addtopic.html', {'form': form, 'topiclist': topiclist})
def topicdetail(request,topic_id):
    topic = get_object_or_404(Topic,pk=topic_id)
    if request.method == 'POST':
      form=InterestForm(request.POST)
      if form.is_valid():
          interest=form.cleaned_data('interested')
          age=form.cleaned_data('age')
          if interest:
              total_age_so_far=topic.num_responses*topic.avg_age
              topic.num_responses +=1
              topic.avg_age = int((total_age_so_far+age)/topic.num_responses)
              topic.save()
              return HttpResponseRedirect(reverse('myapp:topics'))
          else:
              print(form.errors)
              return render(request,'myapp/topicdetail.html',{'topic': topic,'form':form, 'user' : request})
    else:
      print('GET')
      form = InterestForm()
      return render(request, 'myapp/topicdetail.html', {'topic': topic, 'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('myapp:index'))
    else:
        form =RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index')) #
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def mycourse(request):
    l = len(Student.objects.filter(username=request.user.username))
    if l == 1:
        student = Student.objects.get(username=request.user.username)
        course = student.course_set.all()

        return render(request, 'myapp/mycourses.html', {'course': course, 'flag': 0})
    else:

        return render(request, 'myapp/mycourses.html', {'flag': 1})