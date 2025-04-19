from dplmski import create_app, db
from flask_migrate import Migrate
from dplmski.views import views, edit

app = create_app()
migrate = Migrate(app, db)  # Pretpostavljajući da imate definisane db i models u dplmski/__init__.py

app.register_blueprint(views)
app.register_blueprint(edit)
app.register_blueprint(edit, url_prefix='/edit')

if __name__ == '__main__':
    app.run(debug=True)