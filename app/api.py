from fastapi import Depends, FastAPI, Body
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []


app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!."}


@app.get('/posts', tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}


@app.get('/posts/{id}', tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }
    
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

@app.post('/posts', dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_posts(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    # just for example, don't do this in production
    posts.append(post.dict())
    return {
        "data": "post added."
    }


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)

def check_user(data= UserLoginSchema):
    for user in users:
        # just for example, don't do this in production
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
