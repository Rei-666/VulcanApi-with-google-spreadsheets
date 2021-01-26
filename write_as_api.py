from writeas import client
from config import cfg

c = client()
token = cfg['token']
c.setToken(token)

def create_post(description, title):
    post = c.createPost(description, title=title, font="sans")
    return (f"https://write.as/{post['id']}")
