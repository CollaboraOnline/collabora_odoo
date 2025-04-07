
import odoo
import json

from odoo import http
from odoo.http import request
from odoo.addons.collabora_odoo.utils import jwt

class CoolWopiController(odoo.http.Controller):
    # maybe use bearer
    @http.route('/cool/wopi/files/<int:attachment_id>', auth='public')
    def file_info(self, attachment_id, access_token):
        token = jwt.verify_token(request, access_token)
        if 'error' in token:
            return request.make_response(data="Permission denied: {}".format(token['error']), status=401)

        if token['attachment_id'] is not attachment_id:
            return request.make_response("Permission denied. Token invalid for file.", status=403)

        attachments = request.env['ir.attachment'].with_user(token['user'])
        attachment = attachments.browse([attachment_id]).exists()
        if attachment is None:
            return request.not_found()
        attachment = attachment.ensure_one()
        if attachment is None:
            return request.not_found()

        attr = attachment.read(['file_size', 'name'])[0]

        can_read = attachment.has_access("read")
        can_write = attachment.has_access("write")

        res = {
            'BaseFileName': attr['name'],
            'Size': attr['file_size'],
            'UserId': token['user_id'],
            'UserCanWrite': can_write,
        }
        return request.make_json_response(
            data=res,
            status=200,
        )

    def get_file_content(self, attachment_id, user):
        attachments = request.env['ir.attachment'].with_user(user)
        attachment = attachments.browse([attachment_id]).exists().ensure_one()
        if attachment is None:
            return request.not_found()

        #if not attachment.has_access("read"):
        #    return request.make_response("Permission denied.", status=403)

        stream = request.env["ir.binary"]._get_stream_from(attachment, "raw", None, "name", None)
        return stream.get_response(**{"max_age": None})

    def put_file_content(self, attachment_id):
        return request.make_response(
            data="Saved",
            status=200,
            headers=[("Content-Type", "text/plain")]
        )

    # CSRF is disabled as this uses the access_token to authenticate
    @http.route('/cool/wopi/files/<int:attachment_id>/content', auth='public', methods=["GET", "POST"], csrf=False)
    def file_content(self, attachment_id, access_token):
        token = jwt.verify_token(request, access_token)
        if 'error' in token:
            return request.make_response(data="Permission denied: {}".format(token['error']), status=401)

        if token['attachment_id'] is not attachment_id:
            return request.make_response("Permission denied. Token invalid for file.", status=403)

        if request.httprequest.method == "GET":
            return self.get_file_content(attachment_id, token['user'])
        elif request.httprequest.method == "POST":
            return self.put_file_content(attachment_id, token['user'])
        else:
            return request.make_response(data="Error", status=500)
