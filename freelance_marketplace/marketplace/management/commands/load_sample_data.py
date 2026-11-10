"""
Django Management Command to load sample data for testing and demonstrations.
Run with: python manage.py load_sample_data
"""

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from marketplace.models import Profile, Project, Proposal


class Command(BaseCommand):
    help = 'Populates the database with sample users (admin, students, clients), projects, and proposals'

    def handle(self, *args, **options):
        self.stdout.write("Starting sample data loading...")

        # 1. Create Superuser (Admin)
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            Profile.objects.create(user=admin_user, role='Client', bio='Platform Administrator')
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Create Sample Students
        students_data = [
            {
                'username': 'rahul_dev',
                'email': 'rahul@student.edu',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
                'password': 'password123',
                'skills': 'Python, Django, HTML, CSS, JavaScript, SQLite',
                'education': 'B.Tech Computer Science, 3rd Year',
                'bio': 'Passionate full-stack developer with experience in building web applications using Python and Django.'
            },
            {
                'username': 'priya_design',
                'email': 'priya@student.edu',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'password': 'password123',
                'skills': 'Figma, Adobe Photoshop, UI/UX Design, Illustrator, Canva',
                'education': 'B.Des in Visual Communication, 2nd Year',
                'bio': 'Creative visual designer passionate about modern clean branding, poster design, and user interfaces.'
            },
            {
                'username': 'amit_writer',
                'email': 'amit@student.edu',
                'first_name': 'Amit',
                'last_name': 'Verma',
                'password': 'password123',
                'skills': 'Content Writing, Technical Writing, SEO, Proofreading, Research',
                'education': 'B.A. English Literature, Final Year',
                'bio': 'Curious researcher and content creator specializing in tech blogs, articles, and landing page copy.'
            }
        ]

        created_students = []
        for s in students_data:
            user, u_created = User.objects.get_or_create(
                username=s['username'],
                defaults={
                    'email': s['email'],
                    'first_name': s['first_name'],
                    'last_name': s['last_name']
                }
            )
            if u_created:
                user.set_password(s['password'])
                user.save()
                Profile.objects.create(
                    user=user,
                    role='Student',
                    skills=s['skills'],
                    education=s['education'],
                    bio=s['bio']
                )
                self.stdout.write(f"Created student: {s['username']}")
            created_students.append(user)

        # 3. Create Sample Clients
        clients_data = [
            {
                'username': 'tech_solutions',
                'email': 'contact@techsolutions.local',
                'first_name': 'Vikram',
                'last_name': 'Mehta',
                'password': 'password123',
                'bio': 'Small software solutions firm hiring students for web prototypes.'
            },
            {
                'username': 'campus_innovations',
                'email': 'lead@campusinnovations.local',
                'first_name': 'Ananya',
                'last_name': 'Roy',
                'password': 'password123',
                'bio': 'College incubation cell commissioning creative media and software.'
            }
        ]

        created_clients = []
        for c in clients_data:
            user, u_created = User.objects.get_or_create(
                username=c['username'],
                defaults={
                    'email': c['email'],
                    'first_name': c['first_name'],
                    'last_name': c['last_name']
                }
            )
            if u_created:
                user.set_password(c['password'])
                user.save()
                Profile.objects.create(
                    user=user,
                    role='Client',
                    bio=c['bio']
                )
                self.stdout.write(f"Created client: {c['username']}")
            created_clients.append(user)

        # 4. Create Sample Projects
        today = timezone.now().date()
        projects_data = [
            {
                'client': created_clients[0],
                'title': 'Create a College Event Website',
                'description': 'Need a simple, responsive 3-page website for an upcoming college cultural festival. Should include home page, event schedule table, and contact info.',
                'category': 'Web Development',
                'budget': 2500.00,
                'deadline': today + timedelta(days=10),
                'status': 'Open',
            },
            {
                'client': created_clients[0],
                'title': 'Design a Business Logo & Brand Kit',
                'description': 'Looking for a clean, minimalist vector logo and color palette for an educational startup. Deliverables in PNG, SVG, and Figma.',
                'category': 'Graphic Design',
                'budget': 1500.00,
                'deadline': today + timedelta(days=7),
                'status': 'Open',
            },
            {
                'client': created_clients[1],
                'title': 'Build a Personal Portfolio Website',
                'description': 'Develop a personal portfolio website with about section, project showcase gallery, and contact links using HTML, CSS, and Bootstrap.',
                'category': 'Web Development',
                'budget': 2000.00,
                'deadline': today + timedelta(days=14),
                'status': 'Open',
            },
            {
                'client': created_clients[1],
                'title': 'Create Social Media Posters for Tech Fest',
                'description': 'Design 5 eye-catching Instagram and LinkedIn posters announcing coding hackathons, quiz contests, and keynote speakers.',
                'category': 'Graphic Design',
                'budget': 1200.00,
                'deadline': today + timedelta(days=5),
                'status': 'Open',
            },
            {
                'client': created_clients[0],
                'title': 'Write Tech Blog Articles & Website Content',
                'description': 'Write three 800-word articles explaining web development fundamentals for beginners. Engaging, original tone with no plagiarism.',
                'category': 'Content Writing',
                'budget': 1800.00,
                'deadline': today + timedelta(days=8),
                'status': 'Open',
            },
            {
                'client': created_clients[1],
                'title': 'Mobile App UI/UX Mockup in Figma',
                'description': 'Design 6 mobile screens in Figma for a student study group and notes exchange app.',
                'category': 'UI/UX Design',
                'budget': 3000.00,
                'deadline': today + timedelta(days=12),
                'status': 'Assigned',
            }
        ]

        created_projects = []
        for p in projects_data:
            project, p_created = Project.objects.get_or_create(
                title=p['title'],
                client=p['client'],
                defaults={
                    'description': p['description'],
                    'category': p['category'],
                    'budget': p['budget'],
                    'deadline': p['deadline'],
                    'status': p['status']
                }
            )
            if p_created:
                self.stdout.write(f"Created project: {p['title']}")
            created_projects.append(project)

        # 5. Create Sample Proposals
        # Rahul applies to Event Website
        Proposal.objects.get_or_create(
            project=created_projects[0],
            student=created_students[0],
            defaults={
                'description': 'I have built similar college event sites using HTML and Bootstrap. I can finish this in 5 days with full mobile responsiveness.',
                'proposed_amount': 2200.00,
                'estimated_days': 5,
                'status': 'Pending'
            }
        )

        # Priya applies to Logo Design
        Proposal.objects.get_or_create(
            project=created_projects[1],
            student=created_students[1],
            defaults={
                'description': 'As a design student, I specialize in vector logo design with Figma and Illustrator. I will provide 3 initial concepts and unlimited revisions.',
                'proposed_amount': 1500.00,
                'estimated_days': 4,
                'status': 'Pending'
            }
        )

        # Amit applies to Content Writing
        Proposal.objects.get_or_create(
            project=created_projects[4],
            student=created_students[2],
            defaults={
                'description': 'Experienced writing tech blogs for student magazines. Clear, engaging, and well-researched content delivered on time.',
                'proposed_amount': 1800.00,
                'estimated_days': 6,
                'status': 'Pending'
            }
        )

        # Priya's accepted proposal for UI/UX Design project
        Proposal.objects.get_or_create(
            project=created_projects[5],
            student=created_students[1],
            defaults={
                'description': 'Ready to design modern, high-fidelity Figma screens with interactive prototypes.',
                'proposed_amount': 2800.00,
                'estimated_days': 8,
                'status': 'Accepted'
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully loaded all sample data!"))

