import json

from odoo import api, models

class CollaboraDoc(models.Model):
    _name = "collabora.odoo"
    _description = "Collabora Online"

    @api.model
    def can_write_doc(self, attachment_id):
        attachments = self.env['ir.attachment']
        attachment = attachments.browse([attachment_id]).exists()
        if attachment is None:
            return json.dumps({'can_write': false, 'reason': 'attachment not found'})
        try:
            attachment = attachment.ensure_one()
            if attachment is None:
                return json.dumps({'can_write': false, 'reason': 'attachment no unique'})
        except Exception as e:
            # If the file disappear or something an exception is raised.
            # Return not found.
            return json.dumps({'can_write': false, 'reason': 'exception {}'.format(e)})

        can_write = attachment.check_access_rights('write', raise_exception=False)
        return json.dumps({'can_write': can_write, 'reason': 'check access rights'})
