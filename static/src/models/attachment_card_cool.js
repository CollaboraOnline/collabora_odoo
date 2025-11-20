/** @odoo-module **/

/**
 */


import { AttachmentList } from "@mail/core/common/attachment_list";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

const cool_extensions = [
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "odt", "ods", "odp", "odg",
];

patch(AttachmentList.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },

    isCoolAttachment(attachment) {
        return cool_extensions.includes(attachment.extension.toLowerCase());
    },

    async canWrite(attachment) {
        if (!attachment || !this.isCoolAttachment(attachment)) {
            return false;
        }
        let result = await this.orm.call("collabora.odoo", "can_write_doc", [attachment.id]);
        if (result?.reason) {
            console.error("can write error", result.reason);
        }
        return result?.can_write;
    },

    coolOpen(attachment, mode) {
        // Any other value is "read"
        switch (mode) {
        case 'read':
        case 'write':
            break;
        default:
            mode = 'read';
        }
        console.log(`coolOpen called to open ${attachment.id}`);
        window.open(`/collabora_odoo/frame/${attachment.id}/${mode}`, "_blank");
    }
});
