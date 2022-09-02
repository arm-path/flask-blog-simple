from app import app
from blog_blueprint.blog_views import blog
import views

app.register_blueprint(blog, url_prefix='/blog')

if __name__ == "__main__":
    app.run()
