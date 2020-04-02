from django.test import TestCase

#import unittest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.contrib.auth import login

from .views import pozdrav
from .views import check_if_temp_user_exists_and_log_in, get_random_number_as_name, create_anonymous_user, anonymous_or_real


class PozdravTestCase(TestCase):
    def test_pozdrav(self):
        reknu = 'ahoj'
        slovo = pozdrav(reknu)
        #self.assertEqual('vykani', slovo)
        self.assertTrue(slovo == 'tykani' or slovo == 'vykani')
        self.assertTrue(slovo.isalpha())

class AnonymousOrRealTestCase(TestCase):
    def setUp(self):
        User.objects.create(pk=1, username='Joe')

    def test_check_if_temp_user_exists_and_log_in(self):
        request = RequestFactory().get('/')

        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['temporary_user_id'] = 1
        temp_user = request.session['temporary_user_id']

        request.user = temp_user
        #print('Before func ',request.user)

        check_if_temp_user_exists_and_log_in(request)
        #print('After func ',request.user.username)

        logged_user = request.user
        self.assertTrue(logged_user.is_authenticated)
        self.assertEqual(temp_user, logged_user.id)
        self.assertIn(logged_user.username, 'Joe')

    def test_get_random_number_as_name(self):
        rand_number = get_random_number_as_name()
        self.assertTrue(rand_number > 0 and rand_number < 100000)

    def test_create_anonymous_user(self):
        rand_number = get_random_number_as_name()
        user = create_anonymous_user(rand_number)
        self.assertEqual('User', user.first_name)
        self.assertEqual(2, user.id)
        print('uzivatel:', user.id)
        
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_anonymous_or_real(self):
        request = RequestFactory().get('/')
        user = User.objects.get(pk=1)
        
         # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['temporary_user_id'] = 1
        request.user = request.session['temporary_user_id']

        login(request, user)
        anonymous_or_real(request)
        user = request.user
        self.assertTrue(user.is_authenticated)





        print(user.username)

    




"""
def rand_name() -> str :
    return str(randint(0, 100000))
"""

"""

def create_anonymous_user(user: User) -> User:
    rand_numb = rand_name()
    username = rand_name()
    u = User(username=username, first_name='User', last_name=rand_numb)
    u.set_unusable_password()
    u.save()

    u.username = u.id
    u.save()
    return u
user = User()
create_anonymous_user(user)
"""
"""
user = create_anonymous_user(User())
self.assertTrue(user.username > -1)
self.assertTrue(user.username < -100001)
self.assertEqual('User', user.first_name)
"""
"""
if __name__ == '__main__':
    unittest.main()
"""