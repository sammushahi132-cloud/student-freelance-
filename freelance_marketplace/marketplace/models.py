"""
Database Models for Student Freelance Marketplace
Defines: Profile, Project, Proposal
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends Django's built-in User model to store role and background details.
    Each user has exactly one Profile (OneToOneField).
    """
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Client', 'Client'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    skills = models.TextField(blank=True, help_text="List your technical or creative skills (e.g., Python, HTML, UI Design)")
    bio = models.TextField(blank=True, help_text="Brief introduction about yourself")
    education = models.CharField(max_length=200, blank=True, help_text="College, degree, or current academic year")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Project(models.Model):
    """
    Represents a freelance project posted by a Client.
    Linked to the User model via ForeignKey (client).
    """
    CATEGORY_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Graphic Design', 'Graphic Design'),
        ('Content Writing', 'Content Writing'),
        ('Video Editing', 'Video Editing'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Data Entry', 'Data Entry'),
        ('Programming', 'Programming'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.budget} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class Proposal(models.Model):
    """
    Represents a proposal (bid) submitted by a Student for a specific Project.
    Prevent duplicate proposals from the same student for the same project.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='proposals')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    description = models.TextField()
    proposed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate proposals from the same student for the same project
        unique_together = ('project', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"Proposal by {self.student.username} for {self.project.title} - {self.status}"
