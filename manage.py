
### Repair code cause of obsulete library flask script and no migrate command in current flask migrate
import os
from flask_migrate import Migrate
#from flask_script import Manager #no longer required

from run import app
from app import db

app.config.from_object("config.Config")

migrate = Migrate(app, db)
#manager = Manager(app)

# manager.add_command("db", MigrateCommand)

#diubah dari manager ke app soalnya manager udah gadipake
if __name__ == "__main__":
    app.run()