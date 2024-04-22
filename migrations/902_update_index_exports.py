"""Peewee migrations -- 020_update_index_recordings.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import peewee as pw

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql("DROP INDEX exports_start_time_end_time")
    migrator.sql(
        'CREATE INDEX "exports_camera_start_time_end_time" ON "exports" ("camera", "start_time" DESC, "end_time" DESC)'
    )
    migrator.sql(
        'CREATE INDEX "exports_api_exports_summary" ON "exports" ("camera", "start_time" DESC, "duration", "motion", "objects")'
    )
    migrator.sql('CREATE INDEX "exports_start_time" ON "exports" ("start_time")')


def rollback(migrator, database, fake=False, **kwargs):
    pass
