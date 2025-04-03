
import odoo

from odoo import http


class CoolWopiController(odoo.http.Controller):
    # maybe use bearer
    @http.route('/cool/wopi/files/<int:attachment_id>', auth='public')
    def get_file_info(self, attachment_id, access_token):
        return request.not_found()

    @http.route('/cool/wopi/files/<int:attachment_id>/content', auth='public')
    def get_file_content(self, attachment_id, access_token):
        return request.not_found()
