#
# Wisdom of ChatGPT
#

class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        print(f"Connecting to database with connection string: {self.connection_string}")
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


class ServiceFactory:
    def create_database(self, connection_string):
        return Database(connection_string)

    def create_user_service(self, database):
        return UserService(database)


def main():
    # Service factory usage
    service_factory = ServiceFactory()

    # Create database instance
    db = service_factory.create_database("mysql://user:password@localhost:3306/mydatabase")

    # Create user service instance with the injected database
    user_service = service_factory.create_user_service(db)

    # Using the service
    user_service.get_user(1)


if __name__ == "__main__":
    main()
