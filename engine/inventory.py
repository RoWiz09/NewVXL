from engine.cfg.items import ITEMS

class Inventory():
    def __init__(self, slot_count : int):
        self.inventory = []

        for _ in range(slot_count):
            self.inventory.append([-1, 0, {}])
    
    def Add(self, id_ : int, amount : int, data : int):
        if amount == 0:
            return True

        for slot in range(len(self.inventory)):
            if self.inventory[slot][0] == id_ and self.inventory[slot][2] == data:
                self.inventory[slot][0] = id_
                self.inventory[slot][1] += amount
                self.inventory[slot][2] = data

                if self.inventory[slot][1] > ITEMS[id_]["max_stack_size"]:
                    amount = self.inventory[slot][1] - ITEMS[id_]["max_stack_size"]
                    self.inventory[slot][1] = ITEMS[id_]["max_stack_size"]
                else:
                    return True

            elif self.inventory[slot][0] == -1:
                self.inventory[slot][0] = id_
                self.inventory[slot][1] += amount
                self.inventory[slot][2] = data

                if self.inventory[slot][1] > ITEMS[id_]["max_stack_size"]:
                    amount = self.inventory[slot][1] - ITEMS[id_]["max_stack_size"]
                    self.inventory[slot][1] = ITEMS[id_]["max_stack_size"]
                else:
                    return True

        return id_, amount, data

    def Remove(self, id_ : int, amount : int, data : dict):
        if amount == 0:
            return True

        if not self.Check(id_, amount, data):
            return False

        for slot in range(len(self.inventory)):
            if self.inventory[slot][0] == id_ and self.inventory[slot][2] == data:
                self.inventory[slot][1] -= amount

                if self.inventory[slot][1] < 0:
                    amount = abs(self.inventory[slot][1])
                elif self.inventory[slot][1] == 0:
                    self.inventory[slot][0] = -1
                    self.inventory[slot][2] = {}
                    return True
                elif self.inventory[slot][1] > 0:
                    return True

        return False

    def Check(self, id_ : int, amount : int, data : dict):
        if amount == 0:
            return True

        for slot in range(len(self.inventory)):
            if self.inventory[slot][0] == id_ and self.inventory[slot][2] == data:
                if self.inventory[slot][1] >= amount:
                    return True
                else:
                    amount -= self.inventory[slot][1]
            else:
                return False
        return False
