# Декоратор для инъекции зависимости
def inject_dependency(dependency):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Внедрение зависимости и вызов функции
            return func(dependency, *args, **kwargs)

        return wrapper

    return decorator


# Пример класса, представляющего репозиторий пользователей
class UserRepository:
    def get_user(self, user_id):
        # Ваша логика получения пользователя
        return f"User with ID {user_id}"


# Пример класса, который использует инъекцию зависимости через декоратор
class UserService:
    def __init__(self):
        self.user_repository = None  # Зависимость будет внедрена через декоратор

    @inject_dependency(UserRepository)
    def set_user_repository(self, user_repository):
        self.user_repository = user_repository

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)


# Использование
if __name__ == "__main__":
    user_service = UserService()
    user_service.set_user_repository(
        UserRepository
    )  # Внедрение зависимости (заметьте, что UserRepository передается без вызова)
    user = user_service.get_user(1)  # Вызов метода с использованием зависимости
    print(user)  # Вывод: "User with ID 1"
