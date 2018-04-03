#from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse
from .models import Question
from django.template import loader
from django import forms
from .forms import EditForm
from .forms import DeleteForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm
from .forms import LoginForm #all thuis should be on top
from django.contrib.auth import authenticate
from .forms import SignupForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      context = {'latest_question_list': latest_question_list}
      return render(request, 'polls/index.html', context)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# ...
def detail(request, question_id):
    print("going to print question id")
    print(question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# ...
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

from django.views import View
class LoginView(View):
    form_class = LoginForm
    template_name = 'polls/login.html'
    def get(self, request):
        login_form = LoginForm()
        print("hello i am here in login based on class based")
        return render(request, self.template_name, {'form1': login_form})

    def post(self, request, *args, **kwargs):
        print("i m in post method of class based login function")
        login_form = self.form_class(request.POST)
        user_name = login_form.data['user_name']
        pass_word = login_form.data['pass_word']
        print("user name for login is %s" % (user_name))
        print("password for login is %s" % (pass_word))
        if login_form.is_valid():
            print("the form is valid")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                print("username and password is presented in db already")
                return HttpResponseRedirect('/polls/')
            else:
                print("username and password is not presented in that db")
                return HttpResponseRedirect('/login/')
            print("my login is successful")

class GetnameView(View):
    form_class = NameForm
    template_name = 'polls/addquestion.html'
    def get(self, request):
        name_form = NameForm
        print("hello i m going add some question using class based views")
        return render(request, self.template_name, {'form1': name_form})

    def post(self, request, *args, **kwargs):
        print("i m in post method of class based add question function")
        name_form = self.form_class(request.POST)
        print(name_form.data['your_name'])
        if name_form.is_valid():
            print("name form is valid")
            question_obj = Question()
            question_obj.question_text = name_form.data['your_name']
            question_obj.save()
            print("My question name was added successfully")
            return HttpResponseRedirect('/polls/')

class EditView(View):
    form_class = EditForm
    template_name = 'polls/editquestion.html'

    def get(self, request, pk):
        edit_form = EditForm
        a = Question.objects.get(id=pk)
        print("the pk value is in editview ",pk)
        print("filtered question name is   ", a)
        edit_form = EditForm(initial={'edit_text': a})
        print("i am going to edit by using class based views")
        return render(request,self.template_name, {'form1': edit_form, 'pk': pk})

    def post(self, request, pk, **kwargs):
        print("i m in post method of class based edit view")
        edit_form = self.form_class(request.POST)
        edit_text = edit_form.data['edit_text']
        edit_status = edit_form.data['task_status']
        print("edited status is ", edit_status)
        print("the entered value is....... ", edit_text)
        if edit_form.is_valid():
            a = Question.objects.get(id=pk)
            a.question_text = edit_text
            a.status = edit_status
            a.save()
            print("successfully completed")
            return HttpResponseRedirect('/polls/')

class DeleteView(View):
    def get(self, request, pk):
        print("hello i am in delete function on class based pk value is   ", pk)
        b = Question.objects.get(id=pk)
        print("filtered question name for delete is   ", b)
        print(b)
        b.delete()
        print("successfully delete is completed")
        return HttpResponseRedirect('/polls/')

class SignupView(View):
    form_class = SignupForm
    template_name = 'polls/signup.html'

    def get(self, request):
        print("i am in get method of signup function")
        signup_form = SignupForm()
        return render(request, self.template_name, {'form': signup_form})
    def post(self,request, *args, **kwargs):
        sign_form = self.form_class(request.POST)
        user_name = sign_form.data['user_name']
        pass_word = sign_form.data['pass_word']
        print("entered user name  is ", user_name)
        print("the entered password is....... ", pass_word)
        if sign_form.is_valid():
            print("form is valid for signup")
            try:
                user = User.objects.create_user(username=user_name,password=pass_word)
                print("it is in try block of signup")
                print(user)
                user.save()
            except IntegrityError:
                print("exceptions are handled")
                messages.error(request, 'Entered user name is already present in db, give a new user name')
                signup_form = SignupForm()
                return render(request, 'polls/signup.html', {'form': signup_form})
            print("successfully username and password stored in db for signup")
            return HttpResponseRedirect('/polls/')

class LogoutView(View):
    template_name = 'polls/logout.html'
    def get(self, request):
        print("successfully logged out is completed")
        return HttpResponseRedirect('/login/')