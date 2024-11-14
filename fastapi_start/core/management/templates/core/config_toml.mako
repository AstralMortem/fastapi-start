# Main configuration file
DEBUG = true

ALEMBIC_MIGRATIONS_DIR = "@path {this.BASE_DIR}/models/migrations"
ALEMBIC_CONFIG_PATH = "@path {this.ALEMBIC_MIGRATIONS_DIR.parent}/alembic.ini"

DATABASE_URL = "@format sqlite+aiosqlite:///{this.BASE_DIR}/db.sqlite"
BASE_ROUTER = "@format {this.BASE_DIR.name}.routes"