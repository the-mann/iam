from django.urls import path

from . import views


urlpatterns = [
    path('', views.TeacherIndexView.as_view(), name='index'),
    path('', views.TeacherIndexView.as_view(), name='teacher_index'),
    path('class/create', views.ClassCreateView.as_view(), name='class_create'),
    path('class/<int:pk>/create_assignment', views.CreateAssignmentView.as_view(), name='create_assignment'),
    path('send_survey/<int:assignment_id>/pre', views.send_pre_survey, name="send_pre_survey"),
    path('send_survey/<int:assignment_id>/post', views.send_post_survey, name="send_post_survey"),
    #
    path('recipe/add', views.RecipeCreateView.as_view(), name='new_recipe'),
    path('recipe/list', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/fav/<int:id>', views.favorite_add, name='favorite_add'),
    path('recipe/<int:pk>', views.RecipeView.as_view(), name='recipe_detail'),
    path('favorites', views.FavoriteListView.as_view(), name='favorites_list'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path("anonerror/", views.AnonErrorView.as_view(), name="anon_error"),
    path("presurvey/<int:assignment_id>/<int:user_id>", views.PreSurveyView.as_view(), name="pre_survey"),
    path("postsurvey/<int:assignment_id>/<int:user_id>", views.PostSurveyView.as_view(), name="post_survey"),
    path("affirmation/<int:pre>/", views.AffirmationView.as_view(), name="affirmation"),
    path("analytics/<int:pk>/", views.AnalyticsView.as_view(), name="analytics")
]
