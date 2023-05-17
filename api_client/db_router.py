from api_client.models import ClientLog


class ClientLogDbRouter:
    LOG_DB = "logs"
    DEFAULT_DB = "default"

    def db_for_read(self, model, **hints):
        if model == ClientLog:
            return self.LOG_DB
        return None

    def db_for_write(self, model, **hints):
        if model == ClientLog:
            return self.LOG_DB
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if self.LOG_DB == self.DEFAULT_DB:
            return True
        if db == self.LOG_DB and model_name == "clientlog":
            return True
        return db != self.LOG_DB and model_name != "clientlog"
