from multiprocessing import Process, Manager

class WarehouseManager:
    def __init__(self):
        self.data = Manager().dict()

    def process_request(self, request):
        product, action, amount = request
        if action == "receipt":
            if product in self.data:
                self.data[product] += amount
            else:
                self.data[product] = amount
        elif action == "shipment":
            if product in self.data:
                self.data[product] -= amount
                if self.data[product] < 0:
                    self.data[product] = 0

    def handle_request(self, request):
        p = Process(target=self.process_request, args=(request,))
        p.start()
        p.join()

    def run(self, requests):
        for request in requests:
            self.handle_request(request)

if __name__ == "__main__":
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)
