"""
Forms for Student Freelance Marketplace
Handles user registration, login, profile editing, project creation, and proposal submission.
"""

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Project, Proposal


class UserRegistrationForm(forms.Form):
    """
    Form for registering a new user as either a Student or a Client.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., John'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Doe'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a unique username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g., john@example.com'})
    )
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a strong password', 'id': 'reg_password'})
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password', 'id': 'reg_confirm_password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters long.")

        return cleaned_data

    def save(self):
        """
        Creates both the User record with hashed password and the attached Profile.
        """
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        Profile.objects.create(
            user=user,
            role=self.cleaned_data['role']
        )
        return user


class UserLoginForm(forms.Form):
    """
    Form for user login.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password', 'id': 'login_password'})
    )


class StudentProfileForm(forms.ModelForm):
    """
    Form to view and edit student profile details.
    Also handles updating first_name, last_name, and email from the User model.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['skills', 'education', 'bio']
        widgets = {
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Python, Django, HTML, Bootstrap, Figma'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Tech in Computer Science, 3rd Year'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell clients about your background and passion...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return profile


class ProjectForm(forms.ModelForm):
    """
    Form for clients to post and update freelance projects.
    """
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'budget', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Create a College Event Website'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Provide clear details, required features, and deliverables...'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2000', 'min': '1'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget <= 0:
            raise forms.ValidationError("Project budget must be greater than zero.")
        return budget

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline


class ProposalForm(forms.ModelForm):
    """
    Form for students to submit bids/proposals on open projects.
    """
    class Meta:
        model = Proposal
        fields = ['proposed_amount', 'estimated_days', 'description']
        widgets = {
            'proposed_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1800', 'min': '1'}),
            'estimated_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5', 'min': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explain why you are the best fit for this project and your approach...'}),
        }

    def clean_proposed_amount(self):
        amount = self.cleaned_data.get('proposed_amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Proposed amount must be greater than zero.")
        return amount

    def clean_estimated_days(self):
        days = self.cleaned_data.get('estimated_days')
        if days is not None and days <= 0:
            raise forms.ValidationError("Estimated completion time must be at least 1 day.")
        return days

