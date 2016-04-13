#!/usr/bin/env python3
#
# Copyright (C) 2016  minamibashi rearn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import markdown
from markdown.extensions.toc import TocExtension
import konata
from flask import Flask, request, url_for, Response, render_template, abort

app = Flask(__name__)

@app.route('/')
def index():
	pass

@app.route('/tag/<int:tag_id>')
def tag(content_id):
	pass

def kn_print_content(json_data):
	root = json.loads(json_data)
	con = markdown.markdown(root['contents'][0]['context'], extensions=[TocExtension(baselevel=3)], output_format='xhtml5')

	return render_template('contents.html.ja', nav=root['contents'][0]['nav'], contents=root['contents'], site=root['site'], markdown=con)

@app.route('/content/<int:content_id>')
def content(content_id):
	try:
		return kn_print_content(konata.kn_read_content('./tests/kn.sqlite3', content_id))
	except:
		abort(404)

@app.errorhandler(404)
def error_handler(error):
	e = {
		'code': error.code,
		'name': error.name,
		'description': error.description
	}
	e['message'] = '見つかりません。アドレスが間違っていると思われます。'
	return render_template('error.html.ja', error=e), error.code


if __name__ == '__main__':
	app.run(debug=True)
