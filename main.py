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
	site_json = konata.read_site('./tests/kn.sqlite3')
	list_json = konata.contents_list('./tests/kn.sqlite3')
	app.logger.debug(list_json)
	site_dict = json.loads(site_json)
	list_dict = json.loads(list_json)
	return render_template('top.html.ja', list=list_dict, site=site_dict)

@app.route('/tag/')
@app.route('/tag')
def tag_list():
	site_json = konata.read_site('./tests/kn.sqlite3')
	list_json = konata.tags_list('./tests/kn.sqlite3')
	app.logger.debug(list_json)
	site_dict = json.loads(site_json)
	list_dict = json.loads(list_json)
	app.logger.debug(list_dict)
	return render_template('tag_list.html.ja', list=list_dict, site=site_dict)

@app.route('/tag/<int:tag_id>')
def tag(tag_id):
	site_json = konata.read_site('./tests/kn.sqlite3')
	tag_json = konata.read_tag('./tests/kn.sqlite3', tag_id)
	app.logger.debug(tag_json)
	site_dict = json.loads(site_json)
	tag_dict = json.loads(tag_json)
	if tag_dict['tags'] == []:
		abort(404)
	return render_template('tags.html.ja', tag=tag_dict, site=site_dict)


def print_content(contents_json, site_json):
	contens_dict = json.loads(contents_json)
	site_dict = json.loads(site_json)
	con = markdown.markdown(contens_dict['contents'][0]['context'], extensions=[TocExtension(baselevel=3)], output_format='xhtml5')

	return render_template('contents.html.ja', nav=contens_dict['contents'][0]['nav'], contents=contens_dict['contents'], site=site_dict, markdown=con)

@app.route('/content/<int:content_id>')
def content(content_id):
	site_json = konata.read_site('./tests/kn.sqlite3')
	try:
		contents_json = konata.read_content('./tests/kn.sqlite3', content_id)
	except:
		abort(404)
	return print_content(contents_json, site_json)

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
