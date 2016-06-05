"""
Few integration tests to test rest dataset-starred views.
"""
from account.models import Account
from dataset.views import StarredDatasetsViewSet
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from dataset.models import Dataset, StarredDataset


##########################################################################
## User Fixture
##########################################################################


fixtures = {
    'user': {
        'username': 'jdoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'supersecret',
    },
    'dataset': {
        'version': 1,
        'name': 'dataset_1',
        'url': 'http://awesome.com',
        'privacy': 'public'
    }
}


##########################################################################
## Tests for starring a dataset
##########################################################################


class NothingStarredBeforeTest(TestCase):
    """
    User doesn't have any datasets starred before test in this test case
    """

    def setUp(self):
        # create user for testing purposes
        self.view = StarredDatasetsViewSet.as_view({
            'get': 'list',
            'delete': 'destroy',
            'post': 'create'
        })
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(**fixtures['user'])
        account = Account.objects.first()
        fixtures['dataset']['owner'] = account
        self.dataset = Dataset.objects.create(**fixtures['dataset'])

    def test_api_stars_list_empty_success(self):
        # Arrange
        request = self.factory.get('/api/stars/')
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request, format='json')

        # Assert
        assert response.status_code == 200
        assert response.data == []

    def test_api_stars_destroy_not_existing_error(self):
        # Arrange
        request = self.factory.delete('/api/stars/10/')
        force_authenticate(request, user=self.user)

        # Act
        # doing not like in other tests b/c django rest framework can't resolve pk param
        response = self.view(request=request, pk='10')

        # Assert
        assert response.status_code == 404

    def test_api_stars_create_star_success(self):
        # Arrange
        request = self.factory.post('/api/stars/', data={'dataset_id': 1})
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request, format='json')

        # Assert
        assert response.status_code == 201

    def tearDown(self):
        # delete user
        user = User.objects.get(username='jdoe')
        user.delete()
        dataset = Dataset.objects.first()
        dataset.delete()


class StarredDatasetsExistBeforeTest(TestCase):
    """
    User has a dataset starred before test in this test case.
    """

    def setUp(self):
        # create user for testing purposes
        self.view = StarredDatasetsViewSet.as_view({
            'get': 'list',
            'delete': 'destroy',
            'post': 'create'
        })
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(**fixtures['user'])
        account = Account.objects.first()
        fixtures['dataset']['owner'] = account
        self.dataset = Dataset.objects.create(**fixtures['dataset'])
        self.star = StarredDataset.objects.create(**{'user': self.user, 'dataset': self.dataset})

    def test_api_stars_list_success(self):
        # Arrange
        request = self.factory.get('/api/stars/')
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request, format='json')

        # Assert
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_api_stars_create_duplicate_star_error(self):
        # Arrange
        request = self.factory.post('/api/stars/', data={'dataset_id': 1})
        force_authenticate(request, user=self.user)

        # Act
        response = self.view(request, format='json')

        # Assert
        assert response.status_code == 400

    def test_api_stars_destroy_success(self):
        # Arrange
        request = self.factory.delete('/api/stars/{}/'.format(self.dataset.id))
        force_authenticate(request, user=self.user)

        # Act
        # doing not like in other tests b/c django rest framework can't resolve pk param
        response = self.view(request=request, pk=str(self.dataset.id))

        # Assert
        assert response.status_code == 204

    def tearDown(self):
        self.user.delete()
        self.dataset.delete()


class TwoUsersStarringTest(TestCase):
    """
    User has a dataset starred before test in this test case.
    """

    def setUp(self):
        # create user for testing purposes
        self.view = StarredDatasetsViewSet.as_view({
            'get': 'list',
            'delete': 'destroy',
            'post': 'create'
        })
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(**fixtures['user'])
        user2_fixture = fixtures['user']
        user2_fixture['username'] = 'user2'
        self.user2 = User.objects.create_user(**user2_fixture)
        account = Account.objects.first()
        fixtures['dataset']['owner'] = account
        self.dataset1 = Dataset.objects.create(**fixtures['dataset'])
        dataset2_fixture = fixtures['dataset']
        dataset2_fixture['name'] = 'dataset2'
        self.dataset2 = Dataset.objects.create(**dataset2_fixture)

    def test_two_users_starring(self):
        # Arrange
        request1 = self.factory.post('/api/stars/', data={'dataset_id': self.dataset1.id})
        force_authenticate(request1, user=self.user1)
        request2 = self.factory.post('/api/stars/', data={'dataset_id': self.dataset2.id})
        force_authenticate(request2, user=self.user2)

        # Act
        response1 = self.view(request1, format='json')
        response2 = self.view(request2, format='json')

        # Assert
        assert response1.status_code == 201
        assert response2.status_code == 201

        # also check stars that now exist
        stars = list(StarredDataset.objects.all())
        assert len(stars) == 2
        assert next(star for star in stars if star.user.id == self.user1.id)
        assert next(star for star in stars if star.user.id == self.user2.id)

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.dataset1.delete()
        self.dataset2.delete()
