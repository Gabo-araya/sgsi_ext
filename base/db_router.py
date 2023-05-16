from base.models import ClientLog


class LogsDbRouter:
    # TODO: Change this value to "logs" when the automatic creation and migration of this database is implemented  # noqa: E501
    LOG_DB = "default"

    def db_for_read(self, model, **hints):
        if model == ClientLog:
            return self.LOG_DB
        return None

    def db_for_write(self, model, **hints):
        if model == ClientLog:
            return self.LOG_DB
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == self.LOG_DB and model_name == "clientlog":
            return True
        return db != self.LOG_DB and model_name != "clientlog"
