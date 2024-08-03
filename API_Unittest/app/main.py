from fastapi import FastAPI
from app.db import db_chooser, metadata
from app import model
from app.Router import auth, blog, shop, task
from app.Router.shop import products, categories, orders, customers


app = FastAPI()

# Initialize db
def init_db():
    # Initialize auth.db
    auth_engine = db_chooser.get_engine('auth')
    model.Base.metadata.create_all(bind=auth_engine)
    #model.Base.metadata.drop_all(bind=engine)

    # Initialize blog.db
    blog_engine = db_chooser.get_engine('blog')
    model.Base.metadata.create_all(bind=blog_engine)

    # Initialize task.db
    task_engine = db_chooser.get_engine('task')
    model.Base.metadata.create_all(bind=task_engine)

    # Initialize shop.db
    shop_engine = db_chooser.get_engine('shop')
    model.Base.metadata.create_all(bind=shop_engine)

init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(task.router, prefix="/task", tags=["task"])
app.include_router(products.router, prefix="/shop", tags=["shop"])
app.include_router(orders.router, prefix="/shop", tags=["shop"])
app.include_router(categories.router, prefix="/shop", tags=["shop"])
app.include_router(customers.router, prefix="/shop", tags=["shop"])


@app.get("/")
def home():
    return {"Home": "Update your awareness with us"}
