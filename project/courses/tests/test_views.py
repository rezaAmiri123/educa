from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Permission
from courses.models import Subject, Course

User = get_user_model()


class CoursesTestCase(TestCase):
    def get_subject_data(self, num=1):
        return {
            'title': 'title_{}'.format(num),
            'slug': 'slug_{}'.format(num)
        }

    def get_course_data(self, num=1, subject=None, owner=None, students=''):
        return {
            'owner': owner,
            'subject': subject,
            'title': 'course_title_{}'.format(num),
            'slug': 'course_slug_{}'.format(num),
            'overview': 'overview_{}'.format(num),
            'students': students
        }

    def get_module_data(self, num=1, course=None, order=None):
        return {
            'course': course,
            'title': 'title_{}'.format(num),
            'description': 'description_{}'.format(num),
            'order': order
        }

    def get_content_data(self, num=1,):
        pass

    def get_item_base_data(self, num=1, owner=None):
        return {
            'owner': owner,
            'title': 'title_{}'.format(num)
        }

    def get_user_data(self, num=1):
        return {
            'username': 'username_{}'.format(num),
            'email': 'user{}@example.com'.format(num),
            'password': 'p@ssw0rdUser{}'.format(num),
            'first_name': 'first_name_{}'.format(num),
            'last_name': 'last_name_{}'.format(num),
        }

    def login(self, user=None):
        if not user:
            user = self.get_user_data()
        data = {
            'username': user['username'],
            'password': user['password'],
        }
        self.client.login(**data)

    def setUp(self):
        user_data = self.get_user_data()
        user = User.objects.create_user(**user_data)

        permissions = Permission.objects.filter(codename__in=['add_course',
                                                              'change_course',
                                                              'delete_course'])
        user.user_permissions.add(*permissions)
        # create subject
        sub1 = self.get_subject_data()
        subject1 = Subject.objects.create(**sub1)
        # create course
        cour1 = self.get_course_data(subject=subject1, owner=user)
        del cour1['students']
        Course.objects.create(**cour1)

    def test_manage_course_list(self):
        path = reverse('manage_course_list')
        self.login()
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_course_create(self):
        path = reverse('course_create')
        self.login()
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
        subject1 = Subject.objects.latest('pk')
        cour2 = self.get_course_data(num=2, subject=subject1.id)
        del cour2['owner']
        del cour2['students']
        resp = self.client.post(path, cour2)
        self.assertEqual(resp.status_code, 302)
        course2 = Course.objects.get(title=cour2['title'])
        self.assertEqual(course2.__str__(), cour2['title'])

    def test_course_update(self):
        self.login()
        cour = self.get_course_data()
        course = Course.objects.get(title=cour['title'])
        path = reverse('course_edit', args=[course.id])

        # get request
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

        # post request
        subject1 = Subject.objects.latest('pk')
        cour = self.get_course_data(subject=subject1.id)
        del cour['owner']
        del cour['students']
        cour['title'] += 'hi'
        resp = self.client.post(path, cour)
        self.assertEqual(resp.status_code, 302)
        course = Course.objects.get(title=cour['title'])
        self.assertEqual(course.__str__(), cour['title'])

    def test_course_delete(self):
        self.login()
        cour = self.get_course_data()
        course = Course.objects.get(title=cour['title'])
        path = reverse('course_delete', args=[course.id])
        resp = self.client.post(path)
        self.assertEqual(resp.status_code, 302)
        course = Course.objects.first()
        self.assertFalse(course)

    def test_course_module_update(self):
        self.login()
        cour = self.get_course_data()
        course = Course.objects.get(title=cour['title'])
        path = reverse('course_module_update', args=[course.id])
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
        # print(resp.content)


