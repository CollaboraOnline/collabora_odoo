/** @odoo-module **/

/**
 */


import { AttachmentList } from "@mail/core/common/attachment_list";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

const cool_extensions = [
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "odt", "ods", "odp", "odg",
];

patch(AttachmentList.prototype, {
//    components: { ...AttachmentList.components, CoolViewer },

    isCoolAttachment(attachment) {
        return cool_extensions.includes(attachment.extension.toLowerCase());
    },

    coolOpen(attachment) {
        console.log("coolOpen called");
    }
});
