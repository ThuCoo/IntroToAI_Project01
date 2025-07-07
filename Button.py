class Button() :
    def __init__(self, image, pos) :
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, screen) :
        screen.blit(self.image, self.rect)

    def checkForInput(self, position) :
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom) :
            return True
        return False