class Vector:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    # adds two vectors together
    def add(self, vec, component):
        if component == "i":
            self.i += vec.i
        elif component == "j":
            self.j += vec.j
        # if self == vel:
        #     self.limit(component)

    # takes one vector from another
    def subtract(self, vec, component):
        if component == "i":
            self.i -= vec.i
        elif component == "j":
            self.j -= vec.j

    # scales self with another vector
    def scale(self, vec, component, player):
        if not player.canJump:
            deceleration.setVec(1, 0)
        else:
            deceleration.setVec(0.7, 0)
        if component == "i":
            self.i *= vec.i
        if component == "j":
            self.j *= vec.j

    # applies an inverse coefficient to the vector
    def reverse(self, component):
        if component == "i":
            self.i *= -1
        elif component == "j":
            self.j *= -1

    # applies a limit to a vector, so it can't increase
    def limit(self, component):
        if component == "i":
            if vel.i > terminalVel.i > 0:
                self.i = terminalVel.i
            elif vel.i < -terminalVel.i < 0:
                terminalVel.reverse('i')
                self.i = terminalVel.i
                terminalVel.reverse('i')
        elif component == "j":
            self.j = terminalVel.j

    def setVec(self, newI, newJ):
        self.i = newI
        self.j = newJ

    def rotateVec(self):
        newI = -self.j
        newJ = self.i
        self.setVec(newI, newJ)

    def vecAngleChange(self, current, new):
        turns = new.direction - current.direction
        if current.direction == 2 or current.direction == 4:
            turns += 2
        for turn in range(turns):
            self.rotateVec()


gravity = Vector(0, 1)
vel = Vector(0, 0)
posVec = Vector(1000, 400)
acceleration = Vector(0.7, 0)
deceleration = Vector(0.9, 0)
terminalVel = Vector(8, 10)
