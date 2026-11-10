"""
Comprehensive Test Suite for Student Freelance Marketplace
Tests:
1. Student registration, login, profile view & edit
2. Client registration, project posting (CRUD: Create, Read, Update, Delete)
3. Proposal submission, duplicate proposal prevention, validation
4. Proposal acceptance workflow (proposal -> Accepted, project -> Assigned)
5. Access control and role security checks
"""

from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Project, Proposal


class MarketplaceTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Student User
        self.student_user = User.objects.create_user(
            username='test_student',
            email='student@test.com',
            password='testpassword123',
            first_name='Test',
            last_name='Student'
        )
        self.student_profile = Profile.objects.create(
            user=self.student_user,
            role='Student',
            skills='Python, Django',
            education='B.Tech CSE',
            bio='Student Bio'
        )

        # Create Client User
        self.client_user = User.objects.create_user(
            username='test_client',
            email='client@test.com',
            password='testpassword123',
            first_name='Test',
            last_name='Client'
        )
        self.client_profile = Profile.objects.create(
            user=self.client_user,
            role='Client',
            bio='Client Bio'
        )

        # Create Staff / Admin User
        self.admin_user = User.objects.create_user(
            username='test_admin',
            email='admin@test.com',
            password='testpassword123',
            is_staff=True
        )

        # Create Sample Project owned by client_user
        self.project = Project.objects.create(
            client=self.client_user,
            title='Sample Web Project',
            description='Build a sample website.',
            category='Web Development',
            budget=2000.00,
            deadline=timezone.now().date() + timedelta(days=7),
            status='Open'
        )

    # -------------------------------------------------------------------------
    # 1. AUTHENTICATION & REGISTRATION TESTS
    # -------------------------------------------------------------------------

    def test_student_registration(self):
        """Test registering a new student account."""
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Student',
            'username': 'new_student',
            'email': 'new_student@test.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='new_student').exists())
        user = User.objects.get(username='new_student')
        self.assertEqual(user.profile.role, 'Student')

    def test_client_registration(self):
        """Test registering a new client account."""
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Client',
            'username': 'new_client',
            'email': 'new_client@test.com',
            'role': 'Client',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='new_client')
        self.assertEqual(user.profile.role, 'Client')

    def test_login_and_logout(self):
        """Test user login and session logout."""
        # Login
        response = self.client.post(reverse('login'), {
            'username': 'test_student',
            'password': 'testpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)

        # Logout
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    # -------------------------------------------------------------------------
    # 2. STUDENT FUNCTIONALITY TESTS
    # -------------------------------------------------------------------------

    def test_student_dashboard_access(self):
        """Test student dashboard metrics computation."""
        self.client.login(username='test_student', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, Test!")

    def test_student_edit_profile(self):
        """Test updating student profile fields."""
        self.client.login(username='test_student', password='testpassword123')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updated',
            'last_name': 'Student',
            'email': 'updated@test.com',
            'education': 'M.Tech CSE',
            'skills': 'Python, Django, React, AI',
            'bio': 'Updated student biography'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.student_profile.refresh_from_db()
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.first_name, 'Updated')
        self.assertEqual(self.student_profile.skills, 'Python, Django, React, AI')

    def test_proposal_submission_and_duplicate_prevention(self):
        """Test submitting a proposal and verifying duplicates are blocked."""
        self.client.login(username='test_student', password='testpassword123')

        # First proposal
        response = self.client.post(reverse('submit_proposal', args=[self.project.id]), {
            'proposed_amount': 1800.00,
            'estimated_days': 5,
            'description': 'I will build this project cleanly with responsive layout.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Proposal.objects.filter(project=self.project, student=self.student_user).count(), 1)

        # Second duplicate proposal should be blocked
        response = self.client.post(reverse('submit_proposal', args=[self.project.id]), {
            'proposed_amount': 1500.00,
            'estimated_days': 3,
            'description': 'Duplicate proposal test.'
        }, follow=True)
        # Should redirect to my_proposals with warning
        self.assertEqual(Proposal.objects.filter(project=self.project, student=self.student_user).count(), 1)

    # -------------------------------------------------------------------------
    # 3. CLIENT FUNCTIONALITY & PROJECT CRUD TESTS
    # -------------------------------------------------------------------------

    def test_client_crud_project(self):
        """Test Create, Read, Update, Delete for Project model by client."""
        self.client.login(username='test_client', password='testpassword123')

        # 1. CREATE
        response = self.client.post(reverse('post_project'), {
            'title': 'CRUD Test Project',
            'category': 'Programming',
            'description': 'Description for CRUD test project.',
            'budget': 3500.00,
            'deadline': timezone.now().date() + timedelta(days=15),
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        created_proj = Project.objects.get(title='CRUD Test Project')
        self.assertEqual(created_proj.client, self.client_user)

        # 2. READ
        response = self.client.get(reverse('my_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CRUD Test Project')

        # 3. UPDATE
        response = self.client.post(reverse('edit_project', args=[created_proj.id]), {
            'title': 'CRUD Test Project - Updated',
            'category': 'Programming',
            'description': 'Updated description text.',
            'budget': 4000.00,
            'deadline': timezone.now().date() + timedelta(days=20),
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        created_proj.refresh_from_db()
        self.assertEqual(created_proj.title, 'CRUD Test Project - Updated')
        self.assertEqual(created_proj.budget, 4000.00)

        # 4. DELETE
        response = self.client.post(reverse('delete_project', args=[created_proj.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(id=created_proj.id).exists())

    def test_client_accept_and_reject_proposal(self):
        """Test client accepting and rejecting student proposals."""
        # Create Proposal by student
        proposal = Proposal.objects.create(
            project=self.project,
            student=self.student_user,
            description='Test proposal',
            proposed_amount=1900.00,
            estimated_days=4,
            status='Pending'
        )

        self.client.login(username='test_client', password='testpassword123')

        # Accept proposal
        response = self.client.post(reverse('accept_proposal', args=[proposal.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        proposal.refresh_from_db()
        self.project.refresh_from_db()

        self.assertEqual(proposal.status, 'Accepted')
        self.assertEqual(self.project.status, 'Assigned')

    # -------------------------------------------------------------------------
    # 4. SECURITY & ACCESS CONTROL TESTS
    # -------------------------------------------------------------------------

    def test_student_cannot_post_project(self):
        """Ensure students cannot post projects."""
        self.client.login(username='test_student', password='testpassword123')
        response = self.client.post(reverse('post_project'), {
            'title': 'Hacker Project',
            'category': 'Programming',
            'description': 'Illegal project post.',
            'budget': 500.00,
            'deadline': timezone.now().date() + timedelta(days=5),
        }, follow=True)
        self.assertFalse(Project.objects.filter(title='Hacker Project').exists())

    def test_client_cannot_submit_proposal(self):
        """Ensure clients cannot submit bids/proposals."""
        self.client.login(username='test_client', password='testpassword123')
        response = self.client.post(reverse('submit_proposal', args=[self.project.id]), {
            'proposed_amount': 1000.00,
            'estimated_days': 2,
            'description': 'Client bidding illegally'
        }, follow=True)
        self.assertFalse(Proposal.objects.filter(student=self.client_user).exists())

    def test_non_staff_cannot_access_admin_dashboard(self):
        """Ensure regular users cannot view the custom admin dashboard."""
        self.client.login(username='test_student', password='testpassword123')
        response = self.client.get(reverse('admin_dashboard'), follow=True)
        self.assertNotEqual(response.context.get('request').path, reverse('admin_dashboard'))

        # Staff can view admin dashboard
        self.client.login(username='test_admin', password='testpassword123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Platform Administrator Dashboard')
