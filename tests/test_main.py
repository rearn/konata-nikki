import unittest
import main

class test_main(unittest.TestCase):
	def test_make_content(self):
		ret = main.make_content('# テスト\ntestなのですよー\n\n')
		self.assertEqual(ret, '<h1>テスト</h1>\n<p>testなのですよー</p>')


class test_main_flask(unittest.TestCase):

	def setUp(self):
		self.app = main.app.test_client()
		main.konata.test = True

	def tearDown(self):
		pass

	def test_content_list(self):
		rv = self.app.get('/')
		self.assertEqual(rv.status_code, 200)
		self.assertRegex(rv.data.decode(), '<title>kn_test_site</title>')
		self.assertRegex(rv.data.decode(),
			'<a href="/content/1">jubeat_saucer_jubegraph_bot</a>')

	def test_tag_list(self):
		rv = self.app.get('/tag/')
		self.assertEqual(rv.status_code, 200)
		self.assertRegex(rv.data.decode(), '<a href="/tag/1">test')
		self.assertRegex(rv.data.decode(), '<a href="/tag/2">tast2')

	def test_content_success(self):
		rv = self.app.get('/content/1')
		self.assertEqual(rv.status_code, 200)
		self.assertRegex(rv.data.decode(), '<p><a href="/">目次に戻る</a></p>')

	def test_content_error(self):
		rv = self.app.get('/content/42')
		self.assertEqual(rv.status_code, 404)
		self.assertRegex(rv.data.decode(),
			'見つかりません。アドレスが間違っていると思われます。')

	def test_tag_success(self):
		rv = self.app.get('/tag/1')
		self.assertEqual(rv.status_code, 200)
		self.assertRegex(rv.data.decode(),
			'<li><a href="/content/1">jubeat_saucer_jubegraph_bot</a></li>')

	def test_tag_error(self):
		rv = self.app.get('/tag/42')
		self.assertEqual(rv.status_code, 404)
		self.assertRegex(rv.data.decode(),
			'見つかりません。アドレスが間違っていると思われます。')

if __name__ == '__main__':
	unittest.main()
