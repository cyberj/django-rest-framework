from django.conf.urls.defaults import patterns, url
from django.contrib.auth.models import Group, User
# from rest_framework.resources import ModelResource
# from rest_framework.views import ListOrCreateModelView, InstanceModelView
# from rest_framework.tests.models import CustomUser
from rest_framework.tests.testcases import TestModelsTestCase
from rest_framework import serializers
from rest_framework import generics


class GroupSerializer(serializers.ModelSerializer):
    model = Group


class GroupDetailView(generics.InstanceAPIView):
    model = Group
    serializer_class = GroupSerializer


class GroupView(generics.RootAPIView):
    model = Group
    serializer_class = GroupSerializer


# class UserSerializer(serializers.ModelSerializer):
#     model = User

# class UserDetailView(generics.InstanceAPIView):
#     model = User
#     serializer_class = UserSerializer

urlpatterns = patterns('',
    # url(r'^users/$', UserView.as_view(), name="users"),
    # url(r'^users/(?P<pk>[^/]+)/$', UserDetailView.as_view(), name="users-detail"),
    url(r'^groups/$', GroupView.as_view(), name="groups"),
    url(r'^groups/(?P<pk>[^/]+)/$', GroupDetailView.as_view(), name="groups-detail"),

#     url(r'^customusers/$', ListOrCreateModelView.as_view(resource=CustomUserResource), name='customusers'),
#     url(r'^customusers/(?P<id>[0-9]+)/$', InstanceModelView.as_view(resource=CustomUserResource)),
)


class ModelViewTests(TestModelsTestCase):
    """Test the model views rest_framework provides"""
    urls = 'rest_framework.tests.modelviews'

    def test_detail(self):
        """Ensure that a model can be retrieved and has a PUT form"""
        self.assertEqual(0, Group.objects.count())

        gp1 = Group.objects.create(name='foo')
        resp = self.client.get('/groups/%s/' % gp1.pk)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "foo")

        # Test for HTML PUT form
        resp = self.client.get('/groups/%s/' % gp1.pk,
                                HTTP_ACCEPT="text/html")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('name' in resp.context["put_form"].fields)

    def test_creation(self):
        """Ensure that a model object can be created"""
        self.assertEqual(0, Group.objects.count())

        # XXX : Won't work
        # resp = self.client.post('/groups/', {'name': 'foo'})

        # self.assertEqual(resp.status_code, 201)
        # self.assertEqual(1, Group.objects.count())
        # self.assertEqual('foo', Group.objects.all()[0].name)

        # Test for HTML PUT form
        resp = self.client.get('/groups/', HTTP_ACCEPT="text/html")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('name' in resp.context["post_form"].fields)

#     def test_creation_with_m2m_relation(self):
#         """Ensure that a model object with a m2m relation can be created"""
#         group = Group(name='foo')
#         group.save()
#         self.assertEqual(0, User.objects.count())

#         response = self.client.post('/users/', {'username': 'bar', 'password': 'baz', 'groups': [group.id]})

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(1, User.objects.count())

#         user = User.objects.all()[0]
#         self.assertEqual('bar', user.username)
#         self.assertEqual('baz', user.password)
#         self.assertEqual(1, user.groups.count())

#         group = user.groups.all()[0]
#         self.assertEqual('foo', group.name)

#     def test_creation_with_m2m_relation_through(self):
#         """
#         Ensure that a model object with a m2m relation can be created where that
#         relation uses a through table
#         """
#         group = Group(name='foo')
#         group.save()
#         self.assertEqual(0, User.objects.count())

#         response = self.client.post('/customusers/', {'username': 'bar', 'groups': [group.id]})

#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(1, CustomUser.objects.count())

#         user = CustomUser.objects.all()[0]
#         self.assertEqual('bar', user.username)
#         self.assertEqual(1, user.groups.count())

#         group = user.groups.all()[0]
#         self.assertEqual('foo', group.name)
