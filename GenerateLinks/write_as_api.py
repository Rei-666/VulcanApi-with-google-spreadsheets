from writeas import client
from config import cfg

c = client()
token = cfg["WRITE_AS_API_TOKEN"]
c.setToken(token)


def create_post(description, title):
    post = c.createPost(description, title=title, font="sans")
    print(post)
    return f"https://write.as/{post['id']}"
