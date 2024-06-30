import typer
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

cli = typer.Typer()


@cli.command()
def create_user(username: str, password: str):
    with app.app_context():
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        typer.echo(f"User {username} created successfully.")


@cli.command()
def update_user_password(username: str, new_password: str):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            typer.echo(f"Password for user {username} updated successfully.")
        else:
            typer.echo(f"User {username} not found.")


if __name__ == "__main__":
    cli()
