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

import konata
from flask import Flask, request, url_for, Response

app = Flask(__name__)

@app.route('/content/<content_id>')
def kn_html_content(content_id):
	return konata.kn_print_content(konata.kn_read_content('./tests/kn.sqlite3', content_id))

if __name__ == '__main__':
	app.run()
