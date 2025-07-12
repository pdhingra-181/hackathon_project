from django.test import TestCase, Client
from django.urls import reverse
from main.models import SkillProfile

class HomeViewTest(TestCase):
    def setUp(self):
        # Create public profiles
        SkillProfile.objects.create(
            name="Marc Demo",
            is_public=True,
            availability="Weekends",
            skills_offered="JavaScript, Python",
            skills_wanted="Graphic Designer",
            rating=3.9
        )
        SkillProfile.objects.create(
            name="Michell",
            is_public=True,
            availability="Evenings",
            skills_offered="Java",
            skills_wanted="UX Designer",
            rating=2.5
        )
        SkillProfile.objects.create(
            name="Joe Wills",
            is_public=True,
            availability="Mornings",
            skills_offered="HTML, CSS",
            skills_wanted="React",
            rating=4.0
        )

        # Create private profile (should be hidden)
        SkillProfile.objects.create(
            name="Hidden User",
            is_public=False,
            availability="Evenings",
            skills_offered="C++",
            skills_wanted="PHP",
            rating=1.0
        )

        self.client = Client()

    def test_home_page_loads_successfully(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Marc Demo")
        self.assertContains(response, "Michell")
        self.assertContains(response, "Joe Wills")
        self.assertNotContains(response, "Hidden User")  # ensure private profile is not visible

    def test_search_filter(self):
        response = self.client.get(reverse('home'), {'search': 'JavaScript'})
        self.assertContains(response, "Marc Demo")
        self.assertNotContains(response, "Michell")
        self.assertNotContains(response, "Joe Wills")

    def test_availability_filter(self):
        response = self.client.get(reverse('home'), {'availability': 'Mornings'})
        self.assertContains(response, "Joe Wills")
        self.assertNotContains(response, "Marc Demo")
        self.assertNotContains(response, "Michell")

    def test_pagination(self):
        # Add extra profiles to trigger pagination (total = 9)
        for i in range(6):
            SkillProfile.objects.create(
                name=f"User{i}",
                is_public=True,
                availability="Weekends",
                skills_offered="SkillX",
                skills_wanted="SkillY",
                rating=5.0
            )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['users'].paginator.num_pages, 2)
        self.assertTrue(response.context['users'].has_next())
