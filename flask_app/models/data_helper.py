class Helper:
    def __init__(self):
        self.name = "Helper"

    @staticmethod
    def car_data_builder(data):
        car_data = {
        "id": data['cars.id'],
        "year": data['year'],
        "make": data['make'],
        "model": data["model"],
        "trim": data['trim'],
        "color": data["color"],
        "created_at": data['cars.created_at'],
        "updated_at": data['cars.updated_at'],
        "customer_id": data['customer_id']
        }
        return car_data