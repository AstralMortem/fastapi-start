from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from fastapi_start.utils.string import camel2snake


def rename_table(table_name: str):
    if table_name.endswith("_model"):
        table_name = table_name.split("_model")[0]

    if (
        not table_name.endswith("s")
        or not table_name.endswith("es")
        or not table_name.endswith("ies")
    ):
        for i in ["s", "x", "z", "ch", "sh"]:
            if table_name.endswith(i):
                table_name += "es"
                return table_name
        if table_name.endswith("y"):
            table_name += "ies"
            return table_name

        table_name += "s"
    return table_name


class Model(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    def __init_subclass__(cls, **kwargs):
        table_name = camel2snake(cls.__name__)
        cls.__tablename__ = rename_table(table_name)
        super().__init_subclass__(**kwargs)


__all__ = ["Model"]
