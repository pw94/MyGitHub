from django.test import TestCase

from projects.models import Category, MyUser, Project


class CategoryTest(TestCase):

    def test_string_representation(self):
        category = Category(name='category_name', owner=MyUser())
        self.assertEqual(str(category), category.name)


class ProjectTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = MyUser.objects.create(username='User1')
        cls.user2 = MyUser.objects.create(username='User2')
        cat1 = Category.objects.create(name='Cat1', owner=cls.user1)
        cat2 = Category.objects.create(name='Cat2', owner=cls.user2)
        cls.pro1 = Project.objects.create(name='AAA', category=cat1)
        cls.pro2 = Project.objects.create(name='BB', category=cat1)
        cls.pro2.tags.add('EE')
        cls.pro3 = Project.objects.create(name='CC', category=cat2)
        cls.pro3.tags.add('BB', 'CC')
        cls.pro4 = Project.objects.create(name='BB', category=cat2)

    def test_search_by_name(self):
        results = Project.search('AAA', ProjectTest.user1)
        self.assertEqual(results, [ProjectTest.pro1])

    def test_search_by_name_used_by_two_users(self):
        results = Project.search('BB', ProjectTest.user1)
        self.assertEqual(results, [ProjectTest.pro2])

    def test_search_by_name_expect_without_duplicates(self):
        results = Project.search('CC', ProjectTest.user2)
        self.assertEqual(results, [ProjectTest.pro3])

    def test_search_by_common_name_and_tag_expect_one_with_name_first(self):
        results = Project.search('BB', ProjectTest.user2)
        self.assertEqual(results, [ProjectTest.pro4, ProjectTest.pro3])

    def test_search_by_text_with_name_and_tag_expect_one_with_tag_first(self):
        results = Project.search('AAA EE', ProjectTest.user1)
        self.assertEqual(results, [ProjectTest.pro2, ProjectTest.pro1])

    def test_search_by_text_with_tag_and_too_short_name_expect_only_one_with_tag(self):
        results = Project.search('BB ', ProjectTest.user2)
        self.assertEqual(results, [ProjectTest.pro3])

    def test_full_name_representation(self):
        project = Project(name='MyGitHub', url='https://github.com/pw94/MyGitHub')
        self.assertEqual(project.full_name(), 'pw94/MyGitHub')
