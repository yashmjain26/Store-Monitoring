from flask.cli import FlaskGroup
from store_Monitoring.app import app
from store_Monitoring import db
from store_Monitoring.models.user import User

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("update_db")
def update_db():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()