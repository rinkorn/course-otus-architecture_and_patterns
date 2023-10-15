# %%
if __name__ == "__main__":
    class_name = "MyDynamicClass"
    class_definition = (
        f"class {class_name}:\n"
        + "    def __init__(self, value):\n"
        + "        self.value = value\n"
        + "\n"
        + "    def print_value(self):\n"
        + "        print(self.value)\n"
    )

    # Парсинг строки для извлечения имени класса, базовых классов и атрибутов
    namespace = {}
    exec(class_definition, namespace)

    base_classes = ()
    class_attrs = namespace[class_name].__dict__.copy()

    # Создаем класс с использованием функции type
    MyDynamicClass = type(class_name, base_classes, class_attrs)

    # Создаем объект этого класса
    obj = MyDynamicClass("Hello, world!")

    # Вызываем метод объекта
    obj.print_value()
