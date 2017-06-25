class Forager:
    MOVE_MAX_BY_DAY = 1
    STOCK_MAX = 100
    EAT_BY_MOVE = 1
    EAT_BY_DAY = 1
    EAT_MAX_BY_DAY = 5

    def __init__(self, x_init, y_init):
        self.stock = Forager.STOCK_MAX
        self.x_pos = x_init
        self.y_pos = y_init
        self.total_eaten = 0
        self.total_move = 0

    @property
    def is_dead(self):
        return self.stock <= 0

    @property
    def quantity_which_can_be_eat(self):
        return min(Forager.STOCK_MAX - self.stock, Forager.EAT_MAX_BY_DAY)

    def move(self, new_x, new_y):
        move_distance = abs(self.x_pos - new_x) + abs(self.y_pos - new_y)
        if move_distance > Forager.MOVE_MAX_BY_DAY:
            raise ValueError('I cannot move that far')
        self.stock = self.stock - Forager.EAT_BY_MOVE * move_distance
        if self.is_dead:
            return False
        self.x_pos = new_x
        self.y_pos = new_y
        self.total_move = self.total_move + move_distance
        return True

    def eat(self, quantity):
        resource_eat = min(quantity, Forager.STOCK_MAX - self.stock)
        self.stock = self.stock + resource_eat
        self.total_eaten = self.total_eaten + resource_eat

    def sustain(self):
        self.stock = self.stock - Forager.EAT_BY_DAY
        if self.is_dead:
            return False
        return True
