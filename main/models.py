from datetime import datetime
from enum import Enum

import star_ratings.models
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Choices, IntegerChoices, TextChoices


class THREE_RATING(IntegerChoices):
    NOT_REALLY = 0, "Not really..."
    MEH = 1, "Meh..."
    YEAH = 2, "Yeah!"


class SEMESTER_CHOICE(IntegerChoices):
    FALL = 0
    SPRING = 1


class GRADES(IntegerChoices):
    A = 4
    B = 3
    C = 2
    D = 1
    F = 0


class Class(models.Model):
    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    name = models.CharField(max_length=100)

    meeting_time = models.CharField(max_length=200)
    semester = models.IntegerField(choices=SEMESTER_CHOICE.choices, default=SEMESTER_CHOICE.FALL, max_length=100)
    year = models.IntegerField(default=2022)


class Test(models.Model):
    name = models.CharField(max_length=1001)
    date = models.DateField()
    starts_at = models.TimeField()
    length = models.IntegerField()
    pre_survey_sent = models.BooleanField(default=False)
    post_survey_sent = models.BooleanField(default=False)

    klass = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="assignments",
    )


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name", "date", "starts_at", "length"]
        widgets = {
            'date': DatePickerInput(),
            'starts_at': TimePickerInput()
        }

        labels = {
            "length": "Length (minutes)"
        }


class Rating(models.Model):
    # Rating Fields
    confidence = models.IntegerField(choices=THREE_RATING.choices)

    # Metadata fields
    date_rated = models.DateTimeField(datetime.now)
    assignment = models.ForeignKey(Test, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="moods",
    )


class PhoneNumber(models.Model):
    user = models.ForeignKey


class Recipe(models.Model):
    title_text = models.CharField(max_length=200)
    ingredients_list = models.TextField()
    body_text = models.TextField()
    posted_date = models.DateTimeField(default=datetime.now)
    edited_date = models.DateTimeField(default=datetime.now)
    parent = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True,
                               related_name="children")  # reference parent recipe ID
    picture = models.ImageField(null=True, upload_to='photos', blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    favorites = models.ManyToManyField(User, related_name="favorites")

    # THINGS TO THINK ABOUT -
    # what should the picture(s) be
    # what happens when a recipe (particularly a parent recipe) is deleted
    # should a recipe be its own parent by default?

    def __str__(self):
        return self.title_text


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments", null=True)
    body = models.TextField()
    posted_date = models.DateTimeField(default=datetime.now)
    edited_date = models.DateTimeField(null=True)
    recipe = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Start typing...', 'rows': 2}),
        }


class Survey(models.Model):
    confidence = models.IntegerField(choices=THREE_RATING.choices)
    do_my_best = models.IntegerField(choices=THREE_RATING.choices)
    prepared_well = models.IntegerField(choices=THREE_RATING.choices)
    score = models.IntegerField(choices=GRADES.choices)
    datetime = models.DateTimeField(default=datetime.now)


class PreSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["confidence", "do_my_best", "prepared_well", "score"]
        labels = {
            "confidence": "I feel confident",
            "do_my_best": "I can do my best",
            "prepared_well": "I have prepared well",
            "score": "What score do you think you will get?"
        }


class PostSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["confidence", "do_my_best", "prepared_well", "score"]
        labels = {
            "confidence": "I felt confident",
            "do_my_best": "I did my best",
            "prepared_well": "I prepared well",
            "score": "What score do you think you got?"
        }
