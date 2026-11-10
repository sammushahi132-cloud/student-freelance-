"""
Views for Student Freelance Marketplace
Contains function-based views for:
1. Public pages (Home, Projects listing, Project details)
2. Authentication (Register, Login, Logout)
3. Student features (Dashboard, Profile, Edit Profile, Submit Proposal, My Proposals)
4. Client features (Dashboard, Post Project, My Projects, Edit/Delete Project, View Proposals, Accept/Reject Proposal)
5. Admin dashboard (Staff-only summary of system metrics)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import Profile, Project, Proposal
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    StudentProfileForm,
    ProjectForm,
    ProposalForm
)


# ==============================================================================
# 1. PUBLIC VIEWS
# ==============================================================================

def home(request):
    """
    Public landing page showcasing platform highlights, popular categories,
    how the system works, and featured open projects.
    """
    featured_projects = Project.objects.filter(status='Open').order_by('-created_at')[:6]
    total_projects = Project.objects.count()
    total_students = Profile.objects.filter(role='Student').count()
    total_proposals = Proposal.objects.count()

    context = {
        'featured_projects': featured_projects,
        'total_projects': total_projects,
        'total_students': total_students,
        'total_proposals': total_proposals,
    }
    return render(request, 'marketplace/home.html', context)


def projects_list(request):
    """
    Public page to browse open freelance projects with search and category filtering.
    """
    # Only display projects that are open for applications
    projects = Project.objects.filter(status='Open')

    # Search filter by project title or description
    query = request.GET.get('q', '').strip()
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Category filter
    category = request.GET.get('category', '').strip()
    if category:
        projects = projects.filter(category=category)

    # List of categories for filter buttons
    categories = [cat[0] for cat in Project.CATEGORY_CHOICES]

    context = {
        'projects': projects,
        'query': query,
        'selected_category': category,
        'categories': categories,
    }
    return render(request, 'marketplace/projects.html', context)


def project_detail(request, pk):
    """
    Displays full details of a specific project.
    Checks whether the logged-in student has already submitted a proposal.
    """
    project = get_object_or_404(Project, pk=pk)
    has_applied = False
    existing_proposal = None

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        if request.user.profile.role == 'Student':
            existing_proposal = Proposal.objects.filter(project=project, student=request.user).first()
            if existing_proposal:
                has_applied = True

    context = {
        'project': project,
        'has_applied': has_applied,
        'existing_proposal': existing_proposal,
    }
    return render(request, 'marketplace/project_detail.html', context)


# ==============================================================================
# 2. AUTHENTICATION VIEWS
# ==============================================================================

def register_view(request):
    """
    User registration for both Students and Clients.
    Uses Django's User model and creates an associated Profile.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = user.profile.role
            messages.success(request, f"Welcome, {user.first_name or user.username}! Your {role} account has been created.")
            # Automatically log the user in
            login(request, user)
            if role == 'Student':
                return redirect('student_dashboard')
            else:
                return redirect('client_dashboard')
        else:
            messages.error(request, "Please fix the errors in the form below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'marketplace/register.html', {'form': form})


def login_view(request):
    """
    Authenticates user and redirects to role-based dashboard.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        elif hasattr(request.user, 'profile'):
            if request.user.profile.role == 'Student':
                return redirect('student_dashboard')
            return redirect('client_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")

                # Admin/Staff redirection
                if user.is_staff:
                    return redirect('admin_dashboard')

                # Role redirection
                if hasattr(user, 'profile'):
                    if user.profile.role == 'Student':
                        return redirect('student_dashboard')
                    elif user.profile.role == 'Client':
                        return redirect('client_dashboard')

                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'marketplace/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the current user and redirects to home page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


# ==============================================================================
# 3. STUDENT VIEWS (Role: Student)
# ==============================================================================

@login_required
def student_dashboard(request):
    """
    Student dashboard displaying real-time statistics:
    - Total proposals submitted
    - Pending proposals
    - Accepted proposals
    - Rejected proposals
    - Recently available projects
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Student':
        messages.warning(request, "Access restricted to student accounts.")
        return redirect('home')

    user = request.user
    total_proposals = Proposal.objects.filter(student=user).count()
    pending_proposals = Proposal.objects.filter(student=user, status='Pending').count()
    accepted_proposals = Proposal.objects.filter(student=user, status='Accepted').count()
    rejected_proposals = Proposal.objects.filter(student=user, status='Rejected').count()

    recent_projects = Project.objects.filter(status='Open').order_by('-created_at')[:5]

    context = {
        'total_proposals': total_proposals,
        'pending_proposals': pending_proposals,
        'accepted_proposals': accepted_proposals,
        'rejected_proposals': rejected_proposals,
        'recent_projects': recent_projects,
    }
    return render(request, 'marketplace/student_dashboard.html', context)


@login_required
def student_profile(request):
    """
    Displays the student's profile information.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Student':
        messages.warning(request, "Access restricted to student accounts.")
        return redirect('home')

    profile = request.user.profile
    # Parse skills as list for badge display
    skills_list = [s.strip() for s in profile.skills.split(',') if s.strip()] if profile.skills else []

    context = {
        'profile': profile,
        'skills_list': skills_list,
    }
    return render(request, 'marketplace/student_profile.html', context)


@login_required
def edit_profile(request):
    """
    Allows a student to edit their profile details (Name, Email, Skills, Bio, Education).
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Student':
        messages.warning(request, "Access restricted to student accounts.")
        return redirect('home')

    profile = request.user.profile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('student_profile')
        else:
            messages.error(request, "Please correct the errors in the profile form.")
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'marketplace/edit_profile.html', {'form': form})


@login_required
def submit_proposal(request, project_id):
    """
    Allows a student to submit a proposal for an open project.
    Validates:
    - User has Student role
    - Project is Open
    - Student hasn't already applied
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Student':
        messages.error(request, "Only registered students can submit project proposals.")
        return redirect('home')

    project = get_object_or_404(Project, pk=project_id)

    # Check project status
    if project.status != 'Open':
        messages.error(request, "This project is no longer accepting new proposals.")
        return redirect('project_detail', pk=project.id)

    # Prevent duplicate proposals
    if Proposal.objects.filter(project=project, student=request.user).exists():
        messages.warning(request, "You have already submitted a proposal for this project.")
        return redirect('my_proposals')

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.project = project
            proposal.student = request.user
            proposal.status = 'Pending'
            proposal.save()
            messages.success(request, f"Your proposal for '{project.title}' has been submitted successfully!")
            return redirect('my_proposals')
        else:
            messages.error(request, "Please correct the errors in your proposal.")
    else:
        form = ProposalForm()

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'marketplace/submit_proposal.html', context)


@login_required
def my_proposals(request):
    """
    Displays all proposals submitted by the logged-in student.
    Students only see their own proposals.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Student':
        messages.warning(request, "Access restricted to student accounts.")
        return redirect('home')

    proposals = Proposal.objects.filter(student=request.user).select_related('project', 'project__client').order_by('-created_at')

    context = {
        'proposals': proposals,
    }
    return render(request, 'marketplace/my_proposals.html', context)


# ==============================================================================
# 4. CLIENT VIEWS (Role: Client)
# ==============================================================================

@login_required
def client_dashboard(request):
    """
    Client dashboard displaying real-time statistics:
    - Total Projects Posted
    - Open Projects
    - Completed / Assigned Projects
    - Total Proposals Received
    - Recent Projects
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.warning(request, "Access restricted to client accounts.")
        return redirect('home')

    user = request.user
    total_projects = Project.objects.filter(client=user).count()
    open_projects = Project.objects.filter(client=user, status='Open').count()
    completed_projects = Project.objects.filter(client=user, status__in=['Completed', 'Assigned']).count()
    total_proposals = Proposal.objects.filter(project__client=user).count()

    recent_projects = Project.objects.filter(client=user).annotate(
        proposal_count=Count('proposals')
    ).order_by('-created_at')[:5]

    context = {
        'total_projects': total_projects,
        'open_projects': open_projects,
        'completed_projects': completed_projects,
        'total_proposals': total_proposals,
        'recent_projects': recent_projects,
    }
    return render(request, 'marketplace/client_dashboard.html', context)


@login_required
def post_project(request):
    """
    Allows a client to create and post a new freelance project.
    Initial status is set to Open.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Only clients can post freelance projects.")
        return redirect('home')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.status = 'Open'
            project.save()
            messages.success(request, f"Project '{project.title}' posted successfully!")
            return redirect('my_projects')
        else:
            messages.error(request, "Please fix the errors in the project form.")
    else:
        form = ProjectForm()

    return render(request, 'marketplace/post_project.html', {'form': form})


@login_required
def my_projects(request):
    """
    Lists all freelance projects posted by the logged-in client.
    Clients can only see and manage their own projects.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.warning(request, "Access restricted to client accounts.")
        return redirect('home')

    projects = Project.objects.filter(client=request.user).annotate(
        proposal_count=Count('proposals')
    ).order_by('-created_at')

    context = {
        'projects': projects,
    }
    return render(request, 'marketplace/my_projects.html', context)


@login_required
def edit_project(request, pk):
    """
    Allows a client to edit an existing project they own.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Access restricted.")
        return redirect('home')

    project = get_object_or_404(Project, pk=pk, client=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project '{project.title}' updated successfully!")
            return redirect('my_projects')
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = ProjectForm(instance=project)

    return render(request, 'marketplace/edit_project.html', {'form': form, 'project': project})


@login_required
def delete_project(request, pk):
    """
    Allows a client to delete their own project.
    Confirmation is verified before deletion.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Access restricted.")
        return redirect('home')

    project = get_object_or_404(Project, pk=pk, client=request.user)

    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' has been deleted.")
        return redirect('my_projects')

    # If accessed via GET, render a simple confirmation or redirect
    return redirect('my_projects')


@login_required
def view_proposals(request, project_id):
    """
    Displays all proposals submitted by students for a specific client project.
    Allows the client to Accept or Reject proposals.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Access restricted.")
        return redirect('home')

    project = get_object_or_404(Project, pk=project_id, client=request.user)
    proposals = project.proposals.select_related('student', 'student__profile').order_by('-created_at')

    context = {
        'project': project,
        'proposals': proposals,
    }
    return render(request, 'marketplace/view_proposals.html', context)


@login_required
def accept_proposal(request, proposal_id):
    """
    Accepts a student's proposal:
    - Changes the proposal status to Accepted.
    - Changes the project status to Assigned.
    - Prevents other proposals from being accepted for the same project.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Access restricted.")
        return redirect('home')

    proposal = get_object_or_404(Proposal, pk=proposal_id, project__client=request.user)
    project = proposal.project

    if request.method == 'POST':
        # Accept selected proposal
        proposal.status = 'Accepted'
        proposal.save()

        # Update project status to Assigned
        project.status = 'Assigned'
        project.save()

        # Reject other pending proposals for this project to prevent multiple acceptances
        other_pending = project.proposals.filter(status='Pending').exclude(id=proposal.id)
        other_pending.update(status='Rejected')

        messages.success(request, f"Proposal from {proposal.student.username} accepted! Project status is now Assigned.")

    return redirect('view_proposals', project_id=project.id)


@login_required
def reject_proposal(request, proposal_id):
    """
    Rejects a student's proposal:
    - Changes the proposal status to Rejected.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Access restricted.")
        return redirect('home')

    proposal = get_object_or_404(Proposal, pk=proposal_id, project__client=request.user)
    project = proposal.project

    if request.method == 'POST':
        proposal.status = 'Rejected'
        proposal.save()
        messages.info(request, f"Proposal from {proposal.student.username} has been rejected.")

    return redirect('view_proposals', project_id=project.id)


@login_required
def change_project_status(request, project_id, new_status):
    """
    Allows a client to update their project status (e.g. Completed or Closed).
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'Client':
        messages.error(request, "Access restricted.")
        return redirect('home')

    project = get_object_or_404(Project, pk=project_id, client=request.user)
    valid_statuses = [choice[0] for choice in Project.STATUS_CHOICES]

    if new_status in valid_statuses:
        project.status = new_status
        project.save()
        messages.success(request, f"Project status updated to {new_status}.")
    else:
        messages.error(request, "Invalid status choice.")

    return redirect('my_projects')


# ==============================================================================
# 5. ADMIN VIEW (Staff Only)
# ==============================================================================

@login_required
def admin_dashboard(request):
    """
    Custom admin dashboard displaying platform-wide statistics for staff users:
    - Total Students
    - Total Clients
    - Total Projects
    - Total Proposals
    - Recent 5 Projects
    """
    if not request.user.is_staff:
        messages.error(request, "Access restricted to administrators.")
        return redirect('home')

    total_students = Profile.objects.filter(role='Student').count()
    total_clients = Profile.objects.filter(role='Client').count()
    total_projects = Project.objects.count()
    total_proposals = Proposal.objects.count()

    latest_projects = Project.objects.select_related('client').order_by('-created_at')[:5]
    latest_proposals = Proposal.objects.select_related('student', 'project').order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_clients': total_clients,
        'total_projects': total_projects,
        'total_proposals': total_proposals,
        'latest_projects': latest_projects,
        'latest_proposals': latest_proposals,
    }
    return render(request, 'marketplace/admin_dashboard.html', context)
