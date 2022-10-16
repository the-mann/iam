# Create your views here.
import os
import random

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormView
from twilio.rest import Client

from .models import Recipe, CommentForm, Class, Test, TestForm, Survey, PreSurveyForm, PostSurveyForm


class BaseMixin(ContextMixin, View):
    def get_context_data(self, *args, **kwargs):
        x = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:

            if user.socialaccount_set.first() and user.socialaccount_set.first().extra_data and "name" in user.socialaccount_set.first().extra_data:
                x['username'] = user.socialaccount_set.first().extra_data['name']
            else:
                x['username'] = user.username
            x['user'] = request.user
            if len(SocialAccount.objects.filter(user=request.user)) > 0:
                x['extra_data'] = SocialAccount.objects.filter(user=request.user)[0].extra_data
                x['avatar_url'] = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
            else:
                x['extra_data'] = None
                x['avatar_url'] = 'static/assets/img/Default_Profile_Image.png'
        else:
            username = "Not logged in"

        return x


class IndexView(BaseMixin, TemplateView):
    template_name = 'main/index.html'


class RecipeCreateView(BaseMixin, LoginRequiredMixin, CreateView):
    template_name = 'main/recipe.html'
    model = Recipe
    fields = ['title_text', 'ingredients_list', 'body_text', 'picture']
    success_url = reverse_lazy('recipe_list')

    def get_initial(self):
        if 'from' in self.request.GET:
            return model_to_dict(Recipe.objects.get(id=self.request.GET['from']), fields=self.fields)
        else:
            return self.initial

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if 'from' in self.request.POST:
                form.instance.parent = Recipe.objects.get(id=self.request.POST['from'])
            elif 'from' in self.request.GET:
                form.instance.parent = Recipe.objects.get(id=self.request.GET['from'])

            form.instance.owner = self.request.user
            return super().form_valid(form)
        else:
            return HttpResponseRedirect('/anonerror/')


class RecipeListView(BaseMixin, generic.ListView):
    template_name = 'main/recipeList.html'
    context_object_name = 'recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()


class RecipeCommentFormView(SingleObjectMixin, FormView):
    template_name = 'main/recipe_detail.html'
    form_class = CommentForm
    model = Recipe

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/anonerror/')
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        form.instance.owner = self.request.user
        form.instance.recipe = self.object
        form.save()
        return super().form_valid(form)


class RecipeView(View):
    def get(self, request, *args, **kwargs):
        view = RecipeDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RecipeCommentFormView.as_view()
        return view(request, *args, **kwargs)


class RecipeDetailView(BaseMixin, generic.DetailView):
    template_name = 'main/recipe_detail.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


def favorite_add(request, id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe, id=id)
        if recipe.favorites.filter(id=request.user.id).exists():
            recipe.favorites.remove(request.user)
        else:
            recipe.favorites.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('/anonerror/')


class FavoriteListView(BaseMixin, LoginRequiredMixin, generic.ListView):
    template_name = 'main/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            request = self.request
            return Recipe.objects.filter(favorites=request.user)


class SearchResultsView(BaseMixin, generic.ListView):
    model = Recipe
    template_name = 'main/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get("query")
        return Recipe.objects.filter(
            Q(title_text__icontains=query) | Q(ingredients_list__icontains=query) | Q(body_text__icontains=query)
        )


class AnonErrorView(BaseMixin, generic.TemplateView):
    template_name = 'main/anon_error.html'


class TeacherIndexView(BaseMixin, generic.ListView):
    model = Class
    template_name = 'main/teacher/index.html'
    context_object_name = 'classes'


class ClassCreateView(BaseMixin, generic.CreateView):
    template_name = 'main/class/create.html'
    model = Class
    fields = ["professor", "name", "meeting_time", "semester", "year"]
    success_url = reverse_lazy('teacher_index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.professor = self.request.user
        obj.save()
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())


class CreateAssignmentView(BaseMixin, generic.FormView):
    template_name = 'main/class/create_assignment.html'
    form_class = TestForm
    # model = Test
    success_url = reverse_lazy('teacher_index')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.professor = self.request.user
        obj.klass = Class.objects.filter(id=self.kwargs['pk']).first()
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


def send_surveys(request, assignment, pre: bool):
    client = Client(os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_TOKEN"])
    domain = Site.objects.get_current().domain
    for social in SocialAccount.objects.all():
        phone = social.extra_data['phone'] if 'phone' in social.extra_data else None
        if phone is not None:
            survey_url = request.build_absolute_uri(
                reverse_lazy('pre_survey' if pre else 'post_survey',
                        kwargs={"assignment_id": assignment.id, "user_id": social.user_id}))
            message = client.messages.create(
                body=f'Hi {social.extra_data["name"]}, here\'s your {"pre" if pre else "post"} survey for \"{assignment.name}\" at \"{assignment.starts_at.strftime("%-I:%M%p")}\": {survey_url}',
                from_='+13464833186',
                to=social.extra_data['phone']
            )


def send_pre_survey(request, assignment_id):
    assignment = get_object_or_404(Test, id=assignment_id)
    # if assignment.post_survey_sent or "TWILIO_ACCOUNT_ID" not in os.environ and "TWILIO_TOKEN" not in os.environ:
    #     return HttpResponse(status=500)

    send_surveys(request, assignment, True)
    assignment.pre_survey_sent = True
    assignment.save()
    return HttpResponseRedirect(reverse_lazy("teacher_index"))


def send_post_survey(request, assignment_id):
    assignment = get_object_or_404(Test, id=assignment_id)
    # if assignment.post_survey_sent or "TWILIO_ACCOUNT_ID" not in os.environ and "TWILIO_TOKEN" not in os.environ:
    #     return HttpResponse(status=500)

    send_surveys(request, assignment, False)
    assignment.post_survey_sent = True
    assignment.save()
    return HttpResponseRedirect(reverse_lazy("teacher_index"))


class PreSurveyView(BaseMixin, FormView):
    model = Survey
    form_class = PreSurveyForm
    template_name = 'main/survey.html'
    success_url = reverse_lazy("affirmation", kwargs={"pre": 1})


class PostSurveyView(BaseMixin, FormView):
    model = Survey
    form_class = PostSurveyForm
    template_name = 'main/survey.html'
    success_url = reverse_lazy("affirmation", kwargs={"pre": 0})


class AffirmationView(BaseMixin, TemplateView):
    template_name = "main/affirmation.html"

    def get_context_data(self, *args, **kwargs):
        pre = ['I am open to future opportunities\n',  'I am doing my best and that is enough\n',  'I am in charge of my life\n', 'I am calm and content\n', 'I am calm and focused \n', 'I am determined. My hard work powers my success \n', 'I am doing my best and I am proud of what I have accomplished \n', 'I am grateful for where I am today \n', 'I am in control of how I live my life\n', 'I believe in myself. I can overcome obstacles \n', 'I can do hard things \n', "I did my best today and I'll do my best tomorrow\n", 'I have studied hard this semester. I am smart and capable \n', 'I have the potential to succeed\n', 'I know this material \n', 'I possess the strength and ability to accomplish all of my goals and dreams \n', 'I will put my energy into things that matter to me\n', 'â€‹I am adaptable\n', 'Any anxious energy I have will be channeled into a constructive force.\n', 'Everyone around me is supportive and have helped me prepare.\n', 'Grades can never determine my worth.\n', 'Hard work never fails.\n', 'I am a gifted student, and I can succeed in anything.\n', 'I am a good student.\n', 'I am a great student.\n', 'I am a quick learner.\n', 'I am always focused during exams.\n', 'I am calm and focused.\n', 'I am calm, I am intelligent, and I will clear my tests!\n', 'I am capable of earning good grades.\n', 'I am capable.\n', 'I am confident in my test-taking abilities.\n', 'I am focused and well prepared for this exam.\n', 'I am going to ace this exam with ease.\n', 'I am grateful for my academic opportunities.\n', 'I am great at taking exams.\n', 'I am motivated to learn and understand.\n', 'I am my only competitor.\n', 'I am on the journey of becoming a very successful student.\n', 'I am productive.\n', 'I am relaxed during my exams.\n', 'I am smart and have a great memory.\n', 'I am thankful for all the supportive people around me.\n', 'I am thankful for the great education I am receiving.\n', 'I am well prepared for my exams and nothing that comes up will surprise me.\n', 'I am well prepared for the test.\n', 'I am â€‹witty\n', 'I am extraordinary\n', 'I am focused\n', 'I am imaginative\n', 'I am independent\n', 'I am innovative\n', 'I am insightful\n', 'I am intelligent\n', 'I am interesting\n', 'I am intuitive\n', 'I am knowledgable\n', 'I am logical\n', 'I am optimistic\n', 'I am practical\n', 'I am precise\n', 'I am relaxed\n', 'I am reliable\n', 'I am resourceful\n', 'I am sophisticated\n', 'I am strong\n', 'I am studious\n', 'I am thorough\n', 'I am well-rounded\n', 'I am wise\n', 'I believe in myself and my studying capabilities.\n', 'I can do this.\n', 'I don\'t know everything, but I know what I need to know.\n', 'I easily prepare for and take all tests.\n', 'I enjoy being challenged and tested on my knowledge.\n', 'I excel at taking tests\n', 'I feel relaxed and confident when taking tests.\n', 'I focus well during my exams.\n', 'I grow and improve every day.\n', 'I have a great memory and will be able to recall all the information I need during the test.\n', 'I have a growth mindset.\n', 'I have all the information I need to pass this test.\n', 'I have an excellent memory and will be able to recollect all of the material I require throughout the exam.\n', 'I have learned everything I need to know to do well on this test.\n', 'I ignore distractions and remain focused.\n', 'I learn for knowledge, not just for grades.\n', 'I like tests, they are important to measure how much I know.\n', 'I pass exams easily.\n', 'I perform with excellence under stress.\n', 'I possess the strength and ability to accomplish all of my goals and dreams.\n', 'I stay focused while reading, studying, and solving problems.\n', 'I strive to do my best every day.\n', 'I studied hard and will retain all the information I need.\n', 'I studied hard and will retain all the information I need.\n', 'I study hard and learn this material well.\n', 'I will control my breathing and stay calm before and during my test.\n', 'I will control my breathing and stay calm before and during my test.\n', 'I will pass this test and go on to achieve all of my goals.\n', 'I will pass this test and go on to achieve all of my goals.\n', 'I will pass this test and move on to complete all of my objectives.\n', 'I will pass this test.\n', 'I will use any nervous energy I have as a positive force.\n', 'I will use any nervous energy I have as a positive force.\n', 'I worked hard to study and will remember what I need to know.\n', 'I will take one question at a time.\n', 'I am a good student, but  I am a better learner.\n',  'I am grateful for the chance to test my academic strength.\n',  'I am grateful for the opportunity of being educated.\n',  'I am grateful to my parents for believing in me.\n', 'I have done my best to study for this test and am well prepared.\n', 'I have done my best to study for this test and am well prepared.\n', 'I have studied hard for this exam and am absolutely ready.\n', 'In the end, I always do well.\n', 'It is okay to ask for help from others when needed.\n', 'My brain retains much more than I think.\n', 'My confidence amplifies with every correct answer.\n', 'My focus is exemplary.\n', 'Recalling information is just two deep breaths away.\n', 'Studying is fun, and taking a test is just another day going through the material I learned.\n', 'Tests are tough, but my preparation is stronger.\n', 'When I take tests, I feel at ease and confident.']
        post = ['I deserve peace and joy in my life\n', 'I am enough\n', 'I choose to celebrate my good qualities\n', 'I am allowed to have needs and take up space\n', 'I am worthy of respect and kindness\n', 'My needs and wants are important\n', 'I accept myself just the way I am\n', 'I am allowed to take care of myself\n', 'I am allowed to take my own path\n', 'I am at peace with who I am\n', 'I am capable of standing up for myself\n', 'I am letting my thoughts go so that my brain can rest\n', 'I am thankful for this day\n', 'I am worthy of love\n', 'I am courageous\n', 'I am free to create the life I desire\n', 'I appreciate the opportunities I have been given\n', 'I approve of myself\n', 'I deserve success\n', 'I deserve this time to sleep\n', 'I give myself permission to do what is right for me\n', 'I have the ability to recover from difficulties\n', 'I have the power to change\n', 'I have the power to let things go\n', 'I have value\n', 'I love myself fully\n', 'I take care of myself\n', 'I allow myself to take breaks \n', 'My life is full of potential\n', 'My future is bright\n', 'Taking small steps every day can help me achieve big goals\n', 'There are many things that I love about myself\n', 'I am thankful for my healthy body and healthy mind.\n', 'I am forgiving\n', 'I am good-natured\n', 'My grades do not define me.\n', 'Success does not depend on grades.']
        if kwargs['pre'] == 1:
            return {"affirmation": random.choice(pre)}
        else:
            return {"affirmation": random.choice(post)}


class AnalyticsView(BaseMixin, DetailView):
    template_name = "main/analytics.html"
    model = Test
    context_object_name = "assignment"