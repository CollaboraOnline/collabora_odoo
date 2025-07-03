
import odoo
import json
import time
import urllib

from odoo import http
from odoo.http import request
from odoo.addons.collabora_odoo.utils import jwt, discover

class CoolWopiController(odoo.http.Controller):
    # maybe use bearer
    @http.route('/collabora_odoo/wopi/files/<int:attachment_id>', auth='public')
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

        can_read = attachment.check_access_rights('read', raise_exception=False)
        if not can_read:
            return request.make_response(data="Permission denied.", status=403)
        can_write = attachment.check_access_rights('write', raise_exception=False)

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

        if not attachment.check_access_rights('read', raise_exception=False):
            return request.make_response("Permission denied.", status=403)

        stream = request.env["ir.binary"]._get_stream_from(attachment, "raw", None, "name", None)
        return stream.get_response(**{"max_age": None})

    def put_file_content(self, attachment_id):
        return request.make_response(
            data="Saved",
            status=200,
            headers=[("Content-Type", "text/plain")]
        )

    # CSRF is disabled as this uses the access_token to authenticate
    @http.route('/collabora_odoo/wopi/files/<int:attachment_id>/contents', auth='public', methods=["GET", "POST"], csrf=False)
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
            return request.make_response(data="Error, invalid method.", status=500)

    @http.route('/collabora_odoo/frame/<int:attachment_id>', auth='user', website=True)
    def cool_frame(self, attachment_id):
        attachments = request.env['ir.attachment']
        attachment = attachments.browse([attachment_id]).exists()
        if attachment is None:
            return request.not_found()
        attachment = attachment.ensure_one()
        if attachment is None:
            return request.not_found()

        attributes = attachment.read(['name', 'mimetype'])[0]

        access_token_ttl = int(request.env["ir.config_parameter"].sudo().get_param('cool_jwt_ttl'))
        if access_token_ttl == 0:
            access_token_ttl = 86400
        exp = int(time.time()) + access_token_ttl

        user_id = request.env.user.id
        token_data = jwt.make_token(request, user_id, attachment_id, exp)

        if 'error' in token_data:
            return request.make_response(data="Error: {}".format(token_data['error']), status=500)
        if 'token' not in token_data:
            return request.make_response(data="Error, missing token.", status=500)

        access_token = token_data['token']
        wopi_src = request.env["ir.config_parameter"].sudo().get_param('cool_wopi_host_url')
        wopi_src += "/collabora_odoo/wopi/files/" + str(attachment_id)
        try:
            wopi_client = discover.collabora_url(request.env["ir.config_parameter"].sudo().get_param('cool_public_url'), attributes['mimetype'])
        except Exception as e:
            return request.make_response(data="Error getting discovery file: {}.".format(e), status=500)

        return request.render("collabora_odoo.cool_frame", {
            "attachment_id": str(attachment_id),
            "access_token": access_token,
            "access_token_ttl": str(access_token_ttl),
            "closebutton": "true",
            "iframe_style": "",
            "wopi_client": wopi_client,
            "wopi_src": urllib.parse.quote_plus(wopi_src),
            "page_title":  attributes['name'],
        })
