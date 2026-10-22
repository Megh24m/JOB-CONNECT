from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile, JobSeekerSettings, Message
from jobs.models import Job, SavedJob, RecentlyViewed
from applications.models import Application, ApplicationStatusHistory
from notifications.models import Notification
from reviews.models import Review

class Command(BaseCommand):
    help = "Populate the database with sample data including Electrician and local job postings."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database population..."))

        # 1. Create or update Employer accounts
        employers_data = [
            {
                "username": "spark_electricals",
                "email": "contact@sparkelectricals.com",
                "company": "Spark Electrical Services",
            },
            {
                "username": "city_repair_solutions",
                "email": "info@cityrepairs.com",
                "company": "City Home & Repair Solutions",
            },
            {
                "username": "apex_engineering",
                "email": "hr@apexengineering.com",
                "company": "Apex Engineering & Maintenance",
            },
            {
                "username": "metro_retail_group",
                "email": "careers@metroretail.com",
                "company": "Metro Supermarkets & Retail",
            },
            {
                "username": "swift_logistics",
                "email": "jobs@swiftlogistics.com",
                "company": "Swift Express & Logistics",
            },
            {
                "username": "grand_bakery_co",
                "email": "manager@grandbakery.com",
                "company": "Grand Artisanal Bakery",
            },
        ]

        employer_users = {}
        for emp_info in employers_data:
            user, created = User.objects.get_or_create(
                username=emp_info["username"],
                defaults={"email": emp_info["email"], "first_name": emp_info["company"]}
            )
            if created:
                user.set_password("password123")
                user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = "employer"
            profile.verified = True
            profile.save()

            employer_users[emp_info["username"]] = user
            self.stdout.write(f"Employer user ready: {user.username}")

        # 2. Ensure jobseeker accounts exist and have profiles
        seekers = User.objects.filter(profile__role="jobseeker")
        if not seekers.exists():
            default_seeker, _ = User.objects.get_or_create(
                username="testuser_seeker",
                defaults={"email": "seeker@example.com"}
            )
            default_seeker.set_password("password123")
            default_seeker.save()
            Profile.objects.get_or_create(user=default_seeker, defaults={"role": "jobseeker"})
            JobSeekerSettings.objects.get_or_create(user=default_seeker)
            seekers = User.objects.filter(profile__role="jobseeker")

        # 3. Create Jobs (with emphasis on Electrician postings)
        jobs_data = [
            # Electrician Jobs
            {
                "employer": employer_users["spark_electricals"],
                "title": "Senior Residential & Commercial Electrician",
                "company": "Spark Electrical Services",
                "location": "Central City / Downtown",
                "category": "Electrician",
                "job_type": "Full Time",
                "salary": 38000.00,
                "vacancy": 3,
                "description": "Seeking an experienced licensed electrician to inspect, install, repair, and maintain electrical wiring, distribution panels, circuit breakers, and lighting fixtures in commercial and residential properties. Must have 3+ years hands-on experience and knowledge of safety standards."
            },
            {
                "employer": employer_users["apex_engineering"],
                "title": "Licensed Industrial Electrical Technician",
                "company": "Apex Engineering & Maintenance",
                "location": "Industrial Area, Phase 2",
                "category": "Electrician",
                "job_type": "Full Time",
                "salary": 45000.00,
                "vacancy": 2,
                "description": "Looking for a certified industrial electrician proficient with 3-phase power, PLC motor control panels, high voltage transformers, line maintenance, and industrial factory automation troubleshooting."
            },
            {
                "employer": employer_users["city_repair_solutions"],
                "title": "Emergency On-Call Home Repair Electrician",
                "company": "City Home & Repair Solutions",
                "location": "North Suburbs & Surrounding Area",
                "category": "Electrician",
                "job_type": "Daily Wage",
                "salary": 1200.00,
                "vacancy": 5,
                "description": "Urgent hiring for flexible on-call electricians to handle household short circuits, fuse replacements, inverter connections, AC power wiring, and appliance installations. Daily payouts provided."
            },
            {
                "employer": employer_users["spark_electricals"],
                "title": "Junior Electrician / Apprentice Technician",
                "company": "Spark Electrical Services",
                "location": "West Tech Park",
                "category": "Electrician",
                "job_type": "Part Time",
                "salary": 18000.00,
                "vacancy": 4,
                "description": "Great career entry point for ITI diploma holders or apprentice electricians. Work alongside senior electricians to pull wires, install conduit pipes, test circuits, and assist with site installations."
            },

            # Other Local Jobs
            {
                "employer": employer_users["city_repair_solutions"],
                "title": "Master Plumber & Pipe Fitter",
                "company": "City Home & Repair Solutions",
                "location": "Central City",
                "category": "Plumber",
                "job_type": "Full Time",
                "salary": 32000.00,
                "vacancy": 2,
                "description": "Experienced plumber required for residential leakage repairs, sanitary fitting, drainage piping, and water heater installations. Tools provided."
            },
            {
                "employer": employer_users["swift_logistics"],
                "title": "Heavy Goods Vehicle & Transport Driver",
                "company": "Swift Express & Logistics",
                "location": "Logistics Park, East Hub",
                "category": "Driver",
                "job_type": "Full Time",
                "salary": 28000.00,
                "vacancy": 4,
                "description": "Hiring experienced truck drivers with valid commercial driving license. Clean driving record required for inter-city delivery routes."
            },
            {
                "employer": employer_users["swift_logistics"],
                "title": "Express Delivery Rider (Bike Provided)",
                "company": "Swift Express & Logistics",
                "location": "Metropolitan Area",
                "category": "Delivery",
                "job_type": "Full Time",
                "salary": 22000.00,
                "vacancy": 10,
                "description": "Deliver parcels and packages locally. Company bike and fuel allowance provided. Attractive performance incentives offered."
            },
            {
                "employer": employer_users["metro_retail_group"],
                "title": "Supermarket Cashier & Billing Executive",
                "company": "Metro Supermarkets & Retail",
                "location": "City Centre Mall",
                "category": "Supermarket",
                "job_type": "Full Time",
                "salary": 20000.00,
                "vacancy": 3,
                "description": "Handle POS billing counters, manage cash transactions, print invoices, and deliver friendly customer service in a high-volume retail environment."
            },
            {
                "employer": employer_users["metro_retail_group"],
                "title": "Retail Store Sales Associate",
                "company": "Metro Supermarkets & Retail",
                "location": "South Plaza Branch",
                "category": "Retail Shop",
                "job_type": "Part Time",
                "salary": 16500.00,
                "vacancy": 4,
                "description": "Assist retail customers, replenish shelf inventory, maintain store cleanliness, and handle product queries. Flexible evening shifts available."
            },
            {
                "employer": employer_users["grand_bakery_co"],
                "title": "Artisanal Bakery Assistant & Pastry Cook",
                "company": "Grand Artisanal Bakery",
                "location": "Heritage Square",
                "category": "Bakery",
                "job_type": "Full Time",
                "salary": 23000.00,
                "vacancy": 2,
                "description": "Assist master baker in dough preparation, baking fresh breads, decorating cakes, and managing inventory."
            },
            {
                "employer": employer_users["apex_engineering"],
                "title": "Commercial Building Security Officer",
                "company": "Apex Engineering & Maintenance",
                "location": "Tech Park Gate 1",
                "category": "Security",
                "job_type": "Full Time",
                "salary": 21000.00,
                "vacancy": 6,
                "description": "Monitor building visitor entries, operate CCTV systems, perform night patrols, and maintain visitor logs."
            },
            {
                "employer": employer_users["city_repair_solutions"],
                "title": "Office & Commercial Housekeeping Assistant",
                "company": "City Home & Repair Solutions",
                "location": "Downtown Offices",
                "category": "Cleaning",
                "job_type": "Full Time",
                "salary": 17000.00,
                "vacancy": 5,
                "description": "Maintain office cleanliness, sanitize workstations, manage tea/coffee supplies, and oversee general maintenance."
            },
        ]

        created_jobs = []
        for j_info in jobs_data:
            job, created = Job.objects.get_or_create(
                title=j_info["title"],
                company=j_info["company"],
                defaults={
                    "employer": j_info["employer"],
                    "location": j_info["location"],
                    "category": j_info["category"],
                    "job_type": j_info["job_type"],
                    "salary": j_info["salary"],
                    "vacancy": j_info["vacancy"],
                    "description": j_info["description"],
                    "status": "Open",
                }
            )
            created_jobs.append(job)
            self.stdout.write(f"Job posting ready: {job.title} ({job.category})")

        # 4. Create Applications for existing jobseekers
        electrician_job = Job.objects.filter(category="Electrician").first()
        plumber_job = Job.objects.filter(category="Plumber").first()
        delivery_job = Job.objects.filter(category="Delivery").first()

        statuses = ["Applied", "Viewed", "Shortlisted", "Interview", "Selected"]

        for seeker in seekers:
            # Ensure seeker applied to Electrician job and 1-2 others
            for idx, target_job in enumerate([electrician_job, plumber_job, delivery_job]):
                if target_job:
                    status_choice = statuses[idx % len(statuses)]
                    app, app_created = Application.objects.get_or_create(
                        applicant=seeker,
                        job=target_job,
                        defaults={
                            "status": status_choice,
                            "status_changed_at": timezone.now()
                        }
                    )
                    if app_created:
                        ApplicationStatusHistory.objects.create(
                            application=app,
                            status=status_choice
                        )
                        Notification.objects.create(
                            user=seeker,
                            application=app,
                            notification_type="application_submitted",
                            message=f"Your application for {target_job.title} at {target_job.company} is recorded as {status_choice}."
                        )

            # Saved Jobs
            for job_to_save in created_jobs[:3]:
                SavedJob.objects.get_or_create(user=seeker, job=job_to_save)

            # Recently Viewed
            for job_to_view in created_jobs[:5]:
                RecentlyViewed.objects.get_or_create(user=seeker, job=job_to_view)

        # 5. Seed Messages between Employers and Seekers
        primary_seeker = seekers.first()
        spark_emp = employer_users["spark_electricals"]

        if primary_seeker and spark_emp:
            Message.objects.get_or_create(
                sender=spark_emp,
                receiver=primary_seeker,
                content="Hello! We reviewed your profile for the Senior Electrician role. Are you available for an interview tomorrow at 10 AM?"
            )
            Message.objects.get_or_create(
                sender=primary_seeker,
                receiver=spark_emp,
                content="Hello! Yes, absolutely. I have 3 years of residential and commercial wiring experience and can attend."
            )
            Message.objects.get_or_create(
                sender=spark_emp,
                receiver=primary_seeker,
                content="Great! Please visit our Downtown office at 10 AM. Ask for HR."
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated database with Electrician and local job postings!"))
