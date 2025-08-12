/** @odoo-module **/

/**
 */


import { AttachmentList } from "@mail/core/common/attachment_list";
import { patch } from "@web/core/utils/patch";

const cool_extensions = [
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "odt", "ods", "odp", "odg",
];

patch(AttachmentList.prototype, {
    isCoolAttachment(attachment) {
        return cool_extensions.includes(attachment.extension.toLowerCase());
    },

    coolOpen(attachment) {
        console.log(`coolOpen called to open ${attachment.id}`);
        window.open(`/collabora_odoo/frame/${attachment.id}`, "_blank");
    }
});
