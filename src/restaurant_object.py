from abc import ABC, abstractmethod


class RestaurantObject(ABC):

    @abstractmethod
    def update(self):
        pass
