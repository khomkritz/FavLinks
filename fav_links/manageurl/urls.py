from django.urls import path, include
from manageurl import views

urlpatterns = [
    path('create_category',views.CreateCategory.as_view()),
    path('get_category',views.GetCategoryList.as_view()),
    path('get_category/<int:category_id>',views.GetCatagoryID.as_view()),
    path('update_category/<int:category_id>',views.UpdateCategory.as_view()),
    path('delete_category/<int:category_id>', views.DeleteCategory.as_view()),

    path('tag/create', views.CreateTag.as_view()),
    path('tag/get', views.GetTagList.as_view()),
    path('tag/get/<int:tag_id>', views.GetTagID.as_view()),
    path('tag/update/<int:tag_id>', views.UpdateTag.as_view()),
    path('tag/delete/<int:tag_id>', views.DeleteTag.as_view()),
]