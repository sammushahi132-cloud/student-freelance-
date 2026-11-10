"""
URL Configuration for marketplace application
"""

from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),

    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/profile/edit/', views.edit_profile, name='edit_profile'),
    path('projects/<int:project_id>/submit-proposal/', views.submit_proposal, name='submit_proposal'),
    path('student/proposals/', views.my_proposals, name='my_proposals'),

    # Client URLs
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/projects/post/', views.post_project, name='post_project'),
    path('client/projects/', views.my_projects, name='my_projects'),
    path('client/projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('client/projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('client/projects/<int:project_id>/proposals/', views.view_proposals, name='view_proposals'),
    path('client/proposals/<int:proposal_id>/accept/', views.accept_proposal, name='accept_proposal'),
    path('client/proposals/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),
    path('client/projects/<int:project_id>/status/<str:new_status>/', views.change_project_status, name='change_project_status'),

    # Custom Admin Dashboard URL (Staff Only)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

