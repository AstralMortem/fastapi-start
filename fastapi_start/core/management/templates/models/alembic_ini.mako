[alembic]
script_location = ${script_location}

file_template = %%(slug)s-%%(rev)s_%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d

prepend_sys_path = .

truncate_slug_length = 40

version_locations = %(here)s/migrations

version_path_separator = os

output_encoding = utf-8

[post_write_hooks]
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
