from app import app, db
from app.models import User, Post

@app.shell_context_processor    #為flask shell做config setting import 
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}

if __name__ == "__main__":
    app.run('0.0.0.0')