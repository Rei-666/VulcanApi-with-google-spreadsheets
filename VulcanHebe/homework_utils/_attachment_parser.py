from VulcanHebe.models import Attachment


class AttachmentParser:
    def parse_attachment_list(self, attachment_list, homework_id):
        attachments = []
        for attachment in attachment_list:
            attachments.append(self.parse_attachment(attachment, homework_id))
        return attachments

    def parse_attachment(self, attachment, homework_id):
        return Attachment(
            name=attachment.name, link=attachment.link, homework=homework_id
        )
