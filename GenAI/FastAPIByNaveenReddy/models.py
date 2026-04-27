from pydantic import BaseModel

class Product(BaseModel):
    id : int
    name : str
    description : str
    price : float
    quantity : int

    # not required if using pydantic base model becuase pydantic takes care of that
    # def __init__(self, id: int, name: str, description: str, price: float, quantity: int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity
