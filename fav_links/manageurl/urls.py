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

    path('url/create', views.CreateUrl.as_view()),
    path('url/get', views.GetUrlList.as_view()),
    path('url/get/<int:url_id>', views.GetUrlID.as_view()),
    path('url/update/<int:url_id>', views.UpdateUrl.as_view()),
    path('url/delete/<int:url_id>', views.DeleteUrl.as_view()),
    path('url/approve_reject/<int:url_id>', views.ApproveRejectUrl.as_view())
]