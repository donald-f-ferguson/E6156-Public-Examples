class Database:
    def connect(self):
        print("Connecting to the database")
        # Actual database connection logic would go here

    def disconnect(self):
        print("Disconnecting from the database")
        # Actual database disconnection logic would go here


class UserService:
    def __init__(self, database):
        self.database = database

    def get_user(self, user_id):
        self.database.connect()
        # Logic to fetch user from the database based on user_id would go here
        print(f"Fetching user with ID {user_id}")
        self.database.disconnect()


class ServiceLocator:
    _services = {}

    @staticmethod
    def register_service(key, service):
        ServiceLocator._services[key] = service

    @staticmethod
    def get_service(key):
        return ServiceLocator._services.get(key)


def main():
    # Setting up the service locator
    service_locator = ServiceLocator()

    # Registering services in the locator
    db = Database()
    service_locator.register_service("Database", db)

    # Using the service locator to obtain services
    database_from_locator = service_locator.get_service("Database")

    if database_from_locator:
        user_service = UserService(database_from_locator)
        user_service.get_user(1)
    else:
        print("Database service not found in the service locator.")


if __name__ == "__main__":
    main()
