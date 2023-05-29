from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TaskAPIView,TaskDetailAPIView, PostListView,PostCreateView,PostDetailView, PostViewSet

router = DefaultRouter()
router.register(r'posts',PostViewSet,basename="posts")
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/tasks/', TaskAPIView.as_view(), name='task-list'), 
    path('api/tasks/<int:pk>', TaskDetailAPIView.as_view(), name='task-detail'), 
    path('tasks', views.index, name='tasks'),
    path('tasks/search', views.search, name='tasks.search'),
    path('tasks/complete', views.taskCompleted, name='taskCompleted'),
    path('tasks/create', views.create, name='tasks.create'),
    path('tasks/store', views.store, name='tasks.store'),
    path('tasks/update/<int:id>', views.update, name='tasks.update'),
    path('tasks/view/<int:id>', views.view, name='tasks.view'),
    path('tasks/delete/<int:id>', views.task_delete, name='tasks.delete'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    # path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    # path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]

# urlpatterns += router.urls 