from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from kakeibo.models import Kakeibo, Category
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()
faith = 1000

class KakeiboListViewTests(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        #foofoo
        self.username = 'foo@hoge.com'
        self.password = 'secret'
        user = User.objects.create_user(username=self.username,password=self.password)
        #barbar
        self.username2 = 'bar@hoge.com'
        self.password2 = 'secret'
        user2 = User.objects.create_user(username=self.username2,password=self.password2)

        #create Category
        category = Category.objects.create(categorys="TestCategory")
        #create Kakeibo
        self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=category,money=1200,memo="これはとても素晴らしい家計簿",author=user2)
        self.path = reverse('kakeibo:cel_main')
        self.add = reverse('kakeibo:cel_add')

    def test_not_login(self):
        #kakeibo.htmlでログインしてないときに#flagが有るようにしています
        res = self.client.get(self.path)
        self.assertContains(res, '<div id="flag"></div>')

    def test_other_kakeibo(self):
        self.client.login(username=self.username,password=self.password)

        res = self.client.get(self.path)
        self.assertQuerysetEqual(res.context['kakeibo_list'], [])

    def test_kakeibo(self):
        self.client.login(username=self.username2,password=self.password2)

        res = self.client.get(self.path)
        self.assertQuerysetEqual(res.context['kakeibo_list'], ['<Kakeibo: これはとても素晴らしい家計簿>'])

    def test_search(self):
        category = Category.objects.create(categorys="TestCategory")
        time = str(timezone.now())
        date_len = 11
        time = time[:date_len]
        data={
            'date':time,
            'category':category.id,
            'money': 1,
            'memo': 'ピカソの絵 Mark2'
        }
        data2={
            'date':time,
            'category':category.id,
            'money': 10000,
            'memo': '石というかなんというかそれはとても素晴らしい'
        }
        self.client.post(self.add, data=data)
        self.client.post(self.add, data=data2)

        res = self.client.get(self.path, {'key_word':'石'})

        res2 = self.client.get(self.path)

        self.assertNotEqual(res, res2)

class KakeiboCreateView(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.username = 'foo@example.com'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username,password=self.password)
        self.category = Category.objects.create(categorys="TestCategory")
        self.path = reverse('kakeibo:cel_add')

    def test_logged_in(self):
        self.client.login(username=self.username,password=self.password)

        res = self.client.get(self.path)

        self.assertEqual(res.status_code, 200)

    def test_not_logged_in(self):
        res = self.client.get(self.path)

        self.assertEqual(res.status_code, 302)

    def test_post_null(self):
        self.client.login(username=self.username,password=self.password)

        data={}

        res = self.client.post(self.path, data=data)

        self.assertEqual(res.status_code, 200)

    def test_post_data(self):
        self.client.login(username=self.username,password=self.password)

        time = str(timezone.now())
        date_len = 11
        time = time[:date_len] #HTTPは絶対にオブジェクトなんか受け取ってやんない！！！
        data={
            'date':time,
            'category':self.category.id,
            'money': 1000000,
            'memo': 'さつまいもの煮付け -豆板醤を添えて-'
        }

        res = self.client.post(self.path, data=data)
        self.assertEqual(res.status_code, 302)

class KakeiboUpdateView(TestCase):
    def setUp(self):
            super().setUp()
            self.client = Client()

            self.username = 'foo@example.com'
            self.password = 'secret'
            self.user = User.objects.create_user(username=self.username,password=self.password)
            self.category = Category.objects.create(categorys="TestCategory")

            category = Category.objects.create(categorys="TestCategory")
            #create Kakeibo
            self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=category,money=1200,memo="これはとても素晴らしい家計簿",author=self.user)

            self.path = reverse('kakeibo:cel_update', args={self.kakeibo.id})
    def test_not_logged_in(self):
        res = self.client.get(self.path)

        self.assertEqual(res.status_code, 302)
    def test_post_null(self):
            self.client.login(username=self.username,password=self.password)

            data={}

            res = self.client.post(self.path, data=data)

            self.assertEqual(res.status_code, 200)

    def test_post_data(self):
        self.client.login(username=self.username,password=self.password)

        time = str(timezone.now())
        date_len = 11
        time = time[:date_len] #HTTPは絶対にオブジェクトなんか受け取ってやんない！！！
        data={
            'date':time,
            'category':self.category.id,
            'money': 1000000,
            'memo': 'さつまいもの煮付け -豆板醤を添えて-'
        }

        res = self.client.post(self.path, data=data)
        self.assertEqual(res.status_code, 302)

class KakeiboUpdateView(TestCase):
    def setUp(self):
            super().setUp()
            self.client = Client()

            self.username = 'foo@example.com'
            self.password = 'secret'
            self.user = User.objects.create_user(username=self.username,password=self.password)
            self.category = Category.objects.create(categorys="TestCategory")

            category = Category.objects.create(categorys="TestCategory")
            #create Kakeibo
            self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=category,money=1200,memo="これはとても素晴らしい家計簿",author=self.user)

            self.path = reverse('kakeibo:cel_update', args={self.kakeibo.id})
    def test_not_logged_in(self):
        res = self.client.get(self.path)

        self.assertEqual(res.status_code, 302)
    def test_post_null(self):
            self.client.login(username=self.username,password=self.password)

            data={}

            res = self.client.post(self.path, data=data)

            self.assertEqual(res.status_code, 200)

    def test_post_data(self):
        self.client.login(username=self.username,password=self.password)

        time = str(timezone.now())
        date_len = 11
        time = time[:date_len] #HTTPは絶対にオブジェクトなんか受け取ってやんない！！！
        data={
            'date':time,
            'category':self.category.id,
            'money': 1000000,
            'memo': 'さつまいもの煮付け -豆板醤を添えて-'
        }

        res = self.client.post(self.path, data=data)
        self.assertEqual(res.status_code, 302)

class KakeiboDeleteView(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.username = 'foo@example.com'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username,password=self.password)
        self.category = Category.objects.create(categorys="TestCategory")

        category = Category.objects.create(categorys="TestCategory")
        #create Kakeibo
        self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=category,money=1200,memo="これはとても素晴らしい家計簿",author=self.user)

        self.path = reverse('kakeibo:cel_delete', args={self.kakeibo.id})
        self.path404 = reverse('kakeibo:cel_delete', args={999999})

    def test_delete_redicret(self):
        self.client.login(username=self.username,password=self.password)
        res = self.client.post(self.path)

        self.assertEqual(res.status_code, 302)

    def test_delete_404(self):
        self.client.login(username=self.username,password=self.password)
        res = self.client.post(self.path404)

        self.assertEqual(res.status_code, 404)
class KakeiboCSVUploadView(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.username = 'foo@example.com'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username,password=self.password)
        self.category = Category.objects.create(categorys="TestCategory")
        self.path = reverse('kakeibo:cel_import')
        self.path2 = reverse('kakeibo:cel_main')

    def test_create_upload(self):
        inital_data = Category.objects.count()
        self.client.login(username=self.username,password=self.password)
        with open('/src/project2/kakeibo/kakeibo.csv', 'rb') as f:

            #instance
            uploadedfile = SimpleUploadedFile(f.name, f.read())
            files = {'file': uploadedfile}
            res = self.client.post(self.path, files)
            print(res)
        self.assertEqual(Category.objects.count(),inital_data + 5)


    def test_upload(self):
        self.client.login(username=self.username,password=self.password)
        old_main = Kakeibo.objects.all()
        with open('/src/project2/kakeibo/kakeibo.csv', 'rb') as f:

            #instance
            uploadedfile = SimpleUploadedFile(f.name, f.read())
            files = {'file': uploadedfile}
            res = self.client.post(self.path, files)
            print(res)
        new_main = Kakeibo.objects.all()
        self.assertNotEqual(old_main,new_main)

class KakeiboGraphView(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.username = 'foo@example.com'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username,password=self.password)
        self.category = Category.objects.create(categorys="TestCategory")

        #create Kakeibo
        self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=self.category,money=1200,memo="これはとても素晴らしい家計簿",author=self.user)

        self.path = reverse('kakeibo:plot')
        self.subpath = reverse('kakeibo:subplot')

    def test_upload(self):
        self.client.login(username=self.username,password=self.password)
        old_graph = self.client.get(self.path)
        self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=self.category,money=1200,memo="これはとても素晴らしい家計簿",author=self.user)
        new_graph = self.client.get(self.path)
        self.assertNotEqual(old_graph,new_graph)

    def test__subupload(self):
        self.client.login(username=self.username,password=self.password)
        old_graph = self.client.get(self.subpath)
        self.kakeibo = Kakeibo.objects.create(date=timezone.now(),category=self.category,money=1200,memo="これはとても素晴らしい家計簿",author=self.user)
        new_graph = self.client.get(self.subpath)
        self.assertNotEqual(old_graph,new_graph)
