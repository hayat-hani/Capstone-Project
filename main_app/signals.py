from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Skill, Project, Task, Reflection


@receiver(post_save, sender=User)
def create_sample_data(sender, instance, created, **kwargs):
    """create sample data for new users to help them get started with SkillHub"""
    if created:  # only for newly created users
        user = instance
        
        # sample skill 1: web development
        web_skill = Skill.objects.create(
            user=user,
            title="Learn Web Development",
            description="Master the fundamentals of building modern websites and web applications",
            category="Technology"
        )
        
        # tasks for web development skill
        Task.objects.create(
            skill=web_skill,
            title="Complete HTML basics tutorial",
            description="Learn HTML tags, structure, and semantic elements",
            is_completed=True
        )
        
        Task.objects.create(
            skill=web_skill,
            title="Practice CSS styling and layouts",
            description="Build responsive layouts with CSS Grid and Flexbox",
            is_completed=True
        )
        
        Task.objects.create(
            skill=web_skill,
            title="Learn JavaScript fundamentals",
            description="Variables, functions, DOM manipulation, and events",
            is_completed=False
        )
        
        Task.objects.create(
            skill=web_skill,
            title="Build a personal portfolio website",
            description="Create a responsive portfolio showcasing your projects",
            is_completed=False
        )
        
        # reflection for web skill
        Reflection.objects.create(
            skill=web_skill,
            content="Started learning web development and already completed HTML and CSS basics. Really enjoying how creative you can be with styling! Next step is to dive deeper into JavaScript - excited to make my websites interactive."
        )
        
        # sample skill 2: data analysis
        data_skill = Skill.objects.create(
            user=user,
            title="Data Analysis with Python",
            description="Learn to analyze and visualize data using Python libraries",
            category="Technology"
        )
        
        # tasks for data analysis skill
        Task.objects.create(
            skill=data_skill,
            title="Install Python and Jupyter Notebook",
            description="Set up development environment for data analysis",
            is_completed=True
        )
        
        Task.objects.create(
            skill=data_skill,
            title="Learn pandas library basics",
            description="Data manipulation and analysis with pandas DataFrames",
            is_completed=False
        )
        
        Task.objects.create(
            skill=data_skill,
            title="Practice data visualization with matplotlib",
            description="Create charts and graphs to visualize data insights",
            is_completed=False
        )
        
        # sample skill 3: public speaking
        speaking_skill = Skill.objects.create(
            user=user,
            title="Improve Public Speaking",
            description="Build confidence and skills for presenting in front of audiences",
            category="Personal Development"
        )
        
        # tasks for public speaking skill
        Task.objects.create(
            skill=speaking_skill,
            title="Join local Toastmasters club",
            description="Find and attend meetings to practice in supportive environment",
            is_completed=False
        )
        
        Task.objects.create(
            skill=speaking_skill,
            title="Practice daily speech exercises",
            description="Work on voice projection, pacing, and articulation",
            is_completed=False
        )
        
        # sample project 1: personal blog
        blog_project = Project.objects.create(
            user=user,
            title="Personal Tech Blog",
            description="Create and launch a blog to share programming tutorials and tech insights"
        )
        
        # tasks for blog project
        Task.objects.create(
            project=blog_project,
            title="Choose blogging platform and domain name",
            description="Research options like WordPress, Ghost, or static site generators",
            is_completed=True
        )
        
        Task.objects.create(
            project=blog_project,
            title="Design blog layout and branding",
            description="Create logo, color scheme, and overall visual identity",
            is_completed=True
        )
        
        Task.objects.create(
            project=blog_project,
            title="Write first 5 blog posts",
            description="Create content calendar and write initial posts about web development",
            is_completed=False
        )
        
        Task.objects.create(
            project=blog_project,
            title="Set up analytics and SEO",
            description="Install Google Analytics and optimize for search engines",
            is_completed=False
        )
        
        Task.objects.create(
            project=blog_project,
            title="Launch and promote on social media",
            description="Go live and share on LinkedIn, Twitter, and dev communities",
            is_completed=False
        )
        
        # reflection for blog project
        Reflection.objects.create(
            project=blog_project,
            content="Really excited about this blog project! Got the basic setup done and started working on the design. Writing consistently is harder than I expected, but I'm learning a lot by explaining concepts. Planning to share more tutorials about what I'm learning in web development."
        )
        
        # sample project 2: fitness app
        fitness_project = Project.objects.create(
            user=user,
            title="Personal Fitness Tracker App",
            description="Build a mobile-friendly web app to track workouts and fitness goals"
        )
        
        # tasks for fitness project
        Task.objects.create(
            project=fitness_project,
            title="Research fitness tracking features",
            description="Analyze existing apps and define core features needed",
            is_completed=True
        )
        
        Task.objects.create(
            project=fitness_project,
            title="Create wireframes and user interface designs",
            description="Design the app layout and user experience flow",
            is_completed=False
        )
        
        Task.objects.create(
            project=fitness_project,
            title="Set up database schema",
            description="Design models for users, workouts, exercises, and progress tracking",
            is_completed=False
        )
        
        Task.objects.create(
            project=fitness_project,
            title="Implement user authentication",
            description="Build secure login and registration system",
            is_completed=False
        )
        
        # sample project 3: reading challenge
        reading_project = Project.objects.create(
            user=user,
            title="Annual Reading Challenge",
            description="Read 24 books this year across different genres to expand knowledge and perspective"
        )
        
        # tasks for reading project
        Task.objects.create(
            project=reading_project,
            title="Create reading list with diverse genres",
            description="Mix of fiction, non-fiction, biography, and technical books",
            is_completed=True
        )
        
        Task.objects.create(
            project=reading_project,
            title="Set up reading schedule - 2 books per month",
            description="Plan reading time and set monthly deadlines",
            is_completed=True
        )
        
        Task.objects.create(
            project=reading_project,
            title="Read 'Atomic Habits' by James Clear",
            description="First book focusing on personal development and habit formation",
            is_completed=True
        )
        
        Task.objects.create(
            project=reading_project,
            title="Read 'Clean Code' by Robert Martin",
            description="Technical book to improve programming practices",
            is_completed=False
        )
        
        Task.objects.create(
            project=reading_project,
            title="Start a book review journal",
            description="Write notes and reflections after each book",
            is_completed=False
        )
        
        # reflection for reading project
        Reflection.objects.create(
            project=reading_project,
            content="Started my reading challenge strong! 'Atomic Habits' was incredibly useful - already applying some techniques to build better study habits. Looking forward to 'Clean Code' next to improve my programming skills. The key is setting aside 30 minutes each evening for reading."
        )