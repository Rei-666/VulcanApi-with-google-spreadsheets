from pbwrap import Pastebin


class PastebinClient:
    def __init__(self, api_key):
        self.pastebinAPI = Pastebin(api_key)

    def create_post_and_get_url(self, paste_text, title):
        url = self.pastebinAPI.create_paste(paste_text,
                                            api_paste_name=title,
                                            api_paste_private=1)
        return url

