"""
Seed command: create the Founder's Weight community with modules,
members, and businesses.

Run with:
    python manage.py seed_founders_weight

Safe to run multiple times — uses get_or_create throughout.
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Profile
from businesses.models import Business, Category
from communities.models import Community, CommunityModule
from members.models import Membership


MEMBERS = [
    # (username, email, full_name, role, company, location, bio, interests)
    (
        "dera",
        "dera@foundersweight.test",
        "Dera Ndidigwe",
        "Founder & Community Builder",
        "Founder's Weight",
        "Lagos",
        "Building communities that create real economic value for founders across Africa.",
        ["Community", "Entrepreneurship"],
    ),
    (
        "achimba",
        "aj@foundersweight.test",
        "Achimba Juayibim-Enakele",
        "CEO & Founder",
        "Nania by Achimba",
        "Lagos",
        "Lagos-based lifestyle and events company that curates immersive, high-end experiences and products celebrating African culinary heritage and culture.",
        ["Culture", "Lifestyle", "Events"],
    ),
    (
        "adedamola",
        "ao@foundersweight.test",
        "Adedamola Olisa.",
        "Founder",
        "O'shedaa Consult",
        "Abuja",
        "hospitality procurement and lifestyle consulting brand in Lagos that supplies high-end commercial kitchenware while delivering bespoke catering, gifting, and corporate hospitality services.",
        ["Hospitality", "Lifestyle", "Consulting"],
    ),
    (
        "akemi",
        "akemi@foundersweight.test",
        "Akemi Emmanuella Oyinmiebi",
        "Business Owner",
        "Luftballoons & Co",
        "Lagos",
        "Professional event decorator and former reality television pageant contestant based in Lagos.",
        ["Branding", "Creative", "Design"],
    ),
    (
        "aloke",
        "aloke@foundersweight.test",
        "Aloke Nmesoma Constance",
        "Managing Partner",
        "Wear Sonma",
        "Lagos",
        "Fashion designer and entrepreneur who models, customizes, and crafts her own statement apparel lines in Lagos.",
        ["Fashion", "ReadyToWear", "BespokeApparel"],
    ),
    (
        "bayonle",
        "bl@foundersweight.test",
        "Bayonle Lawal",
        "Founder",
        "ONEBRICK Investment Ltd",
        "Abuja",
        "Real estate developer and managing director with over two decades of experience in global and domestic property investment.",
        ["Property", "Real estate"],
    ),
    (
        "chiamaka",
        "cno@foundersweight.test",
        "Chiamaka Nancy Onyejekwe",
        "Head of Growth",
        "GrowthLab Africa",
        "Lagos",
        "Salt Printlady. Client services expert. Graphics enthusiast, and Youth mentor.",
        ["Marketing", "Branding"],
    ),
    (
        "chinonso",
        "coa@foundersweight.test",
        "Chinonso Ofoegbu",
        "Founder",
        "Nita Summer The Label",
        "Lagos",
        "Lagos-based creative entrepreneur and clothing designer building a brand that empowers women worldwide.",
        ["Contemporary", "Womenswear", "Stylish"],
    ),
    (
        "henry",
        "hd@foundersweight.test",
        "Henry Dukuye",
        "Project Manager",
        "Duke Web Tech",
        "Abuja",
        "Agile project manager, software engineer, and digital solutions architect who specializes in translating complex processes into revenue-driving applications.",
        ["SaaSProducts", "TechStartup"],
    ),
    (
        "entia",
        "id@foundersweight.test",
        "Innocentia Duru",
        "Founder",
        "Xafarii",
        "Lagos",
        "Product engineer, machine learning builder, and mixed-media artist building an infrastructure for commerce in Africa.",
        ["ArtificialIntelligence", "SaaS", "Operations"],
    ),
    (
        "judy",
        "jg@foundersweight.test",
        "Judith Gbadebo",
        "Founder",
        "Your Quiet Therapist",
        "Lagos",
        "Licensed clinical psychologist with over eight years of solution-focused therapy experience helping individuals and couples build mental resilience.",
        ["Mental Wellness", "Mindfulness", "Wellness"],
    ),
    (
        "uju",
        "on@foundersweight.test",
        "Obianuju Ndedigwe",
        "Founder",
        "LEAF Africa",
        "Lagos",
        "investment professional and business turnaround specialist with a background in pharmacy who evaluates commercial scaling systems across Africa.",
        ["Market Research", "Health", "Pharmacy"],
    ),
    (
        "oghene",
        "oe@foundersweight.test",
        "Oghenetejiri Emuavobor,",
        "Business Owner",
        "Agba Vendor Ventures",
        "Lagos",
        "independent business owner, retail organizer, and professional advertiser.",
        ["Retail", "Vendors", "Operations"],
    ),
    (
        "tobi",
        "tobi@foundersweight.test",
        "Tobi Adeoye",
        "Founder",
        "BrandQor",
        "Lagos",
        "Multi-hyphenate marketer, brand strategist, copywriter, and professional event host based in Lagos.",
        ["Brand Strategy", "Thought Leadership", "Executive Branding"],
    ),
    (
        "paul",
        "po@foundersweight.test",
        "Paul Oyewusi",
        "Founder",
        "POMA Point",
        "Lagos",
        "Human capital expert, ecosystem mentor, and management consultant holding an Executive MBA from Rome Business School.",
        ["Management Consulting", "Strategy Execution", "Corporate Structure"],
    ),
    (
        "dallas",
        "ocd@foundersweight.test",
        "Onyinyechi C. Dallas",
        "Entreprenuer",
        "The OCD Brand",
        "Lagos",
        "Beauty entrepreneur, educator, and master wig technician who hosts private advanced wig construction masterclasses.",
        ["Luxury Hair", "Beauty", "Wigs"],
    ),
    (
        "lara",
        "oa@foundersweight.test",
        "Omorinsola Alatise",
        "Founder",
        "OMAL Co.",
        "Lagos",
        "Seasoned corporate communications specialist, marketing strategist, and directorship executive with nearly two decades of experience leading education sector public relations",
        ["Corporate Communications", "PR", "Marketing Advisory"],
    ),
    (
        "olly",
        "olly@foundersweight.test",
        "Olayinka Ono",
        "Founder",
        "Itele Apoti Ltd & The Truthstudio",
        "Lagos",
        "Contemporary Nigerian fashion designer, garment engineer, and lifestyle creative who crafts premium clothing designed specifically for everyday longevity.",
        ["Fashion"],
    ),

]

BUSINESSES = [
    # (owner_username, name, category_name, location, tagline, description)
    (
        "dera",
        "Founder's Weight",
        "Community & Media",
        "Lagos",
        "Community for Founders. A Therapy for Business Owners",
        "Founder's Weight is a Nigeria-based quarterly, conversation-led platform and supportive ecosystem that eschews motivational talk to provide entrepreneurs with unscripted, real-world business solutions from industry operators.",
    ),
    (
        "achimba",
        "Nania by Achimba",
        "Lifestyle & Events",
        "Lagos",
        "Immersive Lifestyle Experiences",
        "Nania by Achimba is a Lagos-based lifestyle and events company that curates immersive, high-end experiences and products celebrating African culinary heritage and culture.",
    ),
    (
        "adedamola",
        "O'shedaa Consult",
        "Consulting",
        "Abuja",
        "hospitality procurement and lifestyle consulting",
        "O'shedaa Consult is a premier hospitality procurement and lifestyle consulting brand in Lagos that supplies high-end commercial kitchenware while delivering bespoke catering, gifting, and corporate hospitality services.",
    ),
    (
        "akemi",
        "Luftballoons & Co",
        "Event Decor",
        "Lagos",
        "Aesthetics, Lifestyle",
        "Luftballoonsandco is a premium event styling agency specializing in high-end organic balloon displays, backdrop designs, and surprise room configurations for corporate, intimate, and social celebrations.",
    ),
    (
        "aloke",
        "Wear Sonma",
        "Fashion",
        "Lagos",
        "Ready to wear",
        "Wear Sonma is a modern Nigerian women's fashion label featuring an in-person showroom in Gbagada that offers ready-to-wear and bespoke apparel designed around vibrant colors and perfectly tailored textures.",
    ),
    (
        "bayonle",
        "ONEBRICK Investment Ltd",
        "Real Estate & Property Management",
        "Abuja",
        "Rent to Own",
        "ONEBRICK Investment Ltd is a premier property development firm specializing in residential communities, capital-appreciating land investments, and luxury beach lifestyle destinations along the Lekki-Epe expressway corridor.",
    ),
    (
        "chiamaka",
        "Printnpak",
        "Consulting",
        "Lagos",
        "Branding & Packaging Solutions for SMEs",
        "Printnpak is a Lagos-based custom commercial printing and product packaging business that helps small and medium enterprises protect their products and elevate their brand visibility through high-quality nylon, polybags, and retail carriers.",
    ),
    (
        "chinonso",
        "Nita Summer The Label",
        "Fashion",
        "Lagos",
        "AfroFusionFashion",
        "Nita Summer The Label is an effortlessly chic ready-to-wear and custom women's wear fashion house utilizing bold prints and comfortable silhouettes that transition fluidly from work to social events.",
    ),
    (
        "henry",
        "Duke Web Tech",
        "Technology",
        "Abuja",
        "Accessible Luxury Beauty",
        "Duke Web Tech LTD is a custom software development agency that builds minimum viable products (MVPs), web applications, e-commerce networks, and automated office tools for startups and SMEs.",
    ),
    (
        "entia",
        "Xafarii",
        "Discovery",
        "Lagos",
        "Platform for individuals, businesses, and communities",
        "Xafarii is an artificial intelligence-driven discovery and marketplace intelligence platform built to bridge the visibility gap for hidden local African businesses, communities, and digital value creators.",
    ),
    (
        "judy",
        "Your Quiet Therapist",
        "Health and Wellness",
        "Lagos",
        "Self Therapy",
        "Your Quiet Therapist is an emotional wellness companion brand providing structured journals, therapeutic card decks, and stillness programs to help individuals pause, reflect, and safely process heavy internal thoughts."
        "conversations about building.",
    ),
    (
        "uju",
        "LEAF Africa",
        "Research",
        "Lagos",
        "Data Intelligence for African Market Value Chains",
        "LEAF Africa is a specialized market data intelligence platform dedicated to researching, mapping, and telling the hidden stories of African market value chains and business landscapes.",
    ),
    (
        "oghene",
        "Agba vendor ventures",
        "Vendor Solutions",
        "Lagos",
        "Retail, Vendors",
        "Agba Vendor Ventures operates as a comprehensive offline-friendly digital command center and app that automates bookkeeping, branded PDF invoicing, and debt tracking for retail merchants.",
    ),
    (
        "tobi",
        "BrandQor",
        "Community & Media",
        "Lagos",
        "Executive branding solutions for SMEs",
        "BrandQor is a premium strategic advisory and corporate positioning firm that maps specialized positioning frameworks to transform professionals and executives into global high-authority entities.",
    ),
    (
        "paul",
        "POMA Point",
        "Management Consulting",
        "Lagos",
        "Leadership Alignment",
        "POMA Point LTD is an execution-focused Pan-African management consulting firm that partners with founders and leadership teams to dismantle operational growth bottlenecks and design sustainable corporate structures.",
    ),
    (
        "dallas",
        "The OCD Brand",
        "Wig & Hair Styling",
        "Lagos",
        "Beauty",
        "The OCD Brand is an e-commerce beauty and personal care line specializing in premium luxury hair extensions, custom lace wigs, and specialty restorative hair and body oils.",
    ),
    (
        "lara",
        "OMAL Co.",
        "Public Relations & Marketing",
        "Lagos",
        "PR",
        "Operating as a high-level private marketing advisory, her consulting framework helps corporate brands, academic groups, and growing SMEs align their communication structures and build public trust.",
    ),
    (
        "olly",
        "Itele Apoti Ltd & The Truthstudio",
        "Community & Media",
        "Lagos",
        "Community for Founders",
        "Operating jointly as a custom atelier and creative agency, Itele Apoti Ltd produces high-end linen collections and luxury bespoke menswear under the thematic banner Made in Lagos for worthy men, while the visual wing, The Truthstudio, designs complementary minimalist streetwear",
        
    ),
]

# Modules: (key, is_active, order)
MODULES = [
    ("home", True, 0),
    ("members", True, 1),
    ("events", True, 2),
    ("businesses", True, 3),
    ("discussions", True, 4),
    ("shop", False, 5),
    ("jobs", False, 6),
    ("projects", False, 7),
    ("resources", False, 8),
]


class Command(BaseCommand):
    help = "Seed the Founder's Weight community with members and businesses."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding Founder's Weight..."))

        # ---- Community ----
        community, created = Community.objects.get_or_create(
            slug="founders-weight",
            defaults={
                "name": "Founder's Weight",
                "tagline": "Building a stronger network for founders.",
                "description": (
                    "Founder's Weight is a community of founders, entrepreneurs, "
                    "and business leaders building across Africa."
                ),
                "location": "Lagos",
                "is_active": True,
            },
        )
        self.stdout.write(
            f"  Community: {community.name} ({'created' if created else 'exists'})"
        )

        # ---- Modules ----
        for key, is_active, order in MODULES:
            CommunityModule.objects.get_or_create(
                community=community,
                key=key,
                defaults={
                    "is_active": is_active,
                    "order": order,
                    "coming_soon_message": "Coming soon",
                },
            )
        self.stdout.write(f"  Modules: {len(MODULES)} ensured")

        # ---- Categories ----
        category_names = sorted({b[2] for b in BUSINESSES})
        for name in category_names:
            Category.objects.get_or_create(name=name)
        self.stdout.write(f"  Categories: {len(category_names)} ensured")

        # ---- Members ----
        for username, email, full_name, role, company, location, bio, interests in MEMBERS:
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": full_name.split()[0],
                    "last_name": " ".join(full_name.split()[1:]),
                },
            )
            if user_created:
                user.set_password("foundersweight2024")
                user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.full_name = full_name
            profile.role = role
            profile.company = company
            profile.location = location
            profile.bio = bio
            profile.interests = interests
            profile.save()

            Membership.objects.get_or_create(
                user=user,
                community=community,
                defaults={"role": "member", "status": "active"},
            )

        self.stdout.write(f"  Members: {len(MEMBERS)} ensured")

        # ---- Businesses ----
        for owner_username, name, category_name, location, tagline, description in BUSINESSES:
            try:
                owner = User.objects.get(username=owner_username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"  Skipping {name} — owner {owner_username} not found"
                    )
                )
                continue

            category = Category.objects.filter(name=category_name).first()

            business, biz_created = Business.objects.get_or_create(
                name=name,
                defaults={
                    "owner": owner,
                    "category": category,
                    "location": location,
                    "tagline": tagline,
                    "description": description,
                    "visibility": "community",
                    "is_active": True,
                },
            )
            business.communities.add(community)

        self.stdout.write(f"  Businesses: {len(BUSINESSES)} ensured")

        self.stdout.write(self.style.SUCCESS("\nDone. Founder's Weight is seeded."))
        self.stdout.write(
            "  Login with any member: username above, password: foundersweight2024"
        )