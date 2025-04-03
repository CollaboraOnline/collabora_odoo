
import odoo
import json

from odoo import http
from odoo.http import request

class CoolWopiController(odoo.http.Controller):
    # maybe use bearer
    @http.route('/cool/wopi/files/<int:attachment_id>', auth='public')
    def file_info(self, attachment_id, access_token):
        if not self.verify_token(access_token):
            return request.make_response(data="Permission denied", status=410)

        res = {
            'BaseFileName': 'test.txt',
            'Size': 11,
            'UserId': 1,
            'UserCanWrite': True,
        }
        return request.make_json_response(
            data=res,
            status=200,
        )

    def get_file_content(self):
        return request.make_response(
            data="Hello world",
            status=200,
            headers=[("Content-Type", "text/plain")]
        )

    def put_file_content(self):
        return request.make_response(
            data="Saved",
            status=200,
            headers=[("Content-Type", "text/plain")]
        )

    def verify_token(self, token):
        return True

    # CSRF is disabled as this uses the access_token to authenticate
    @http.route('/cool/wopi/files/<int:attachment_id>/content', auth='public', methods=["GET", "POST"], csrf=False)
    def file_content(self, attachment_id, access_token):
        if not self.verify_token(access_token):
            return request.make_response(data="Permission denied", status=410)

        if request.httprequest.method == "GET":
            return self.get_file_content()
        elif request.httprequest.method == "POST":
            return self.put_file_content()
        else:
            return request.make_response(data="Error", status=500)
