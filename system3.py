# Printing:
# system
# system.pendulum
#   - system.pendulum.gravity -> system.gravity.value = 0
# system.pendulum.mass
#   - system.pendulum.mass.force = 0
#   - system.pendulum.mass.velocity = 0
#   - system.pendulum.mass.position = 0.1
#   - system.pendulum.mass.acceleration = 0
# system.pendulum.spring
#   - system.pendulum.spring.displacement -> system.pendulum.mass.position = 0.1
#   - system.pendulum.spring.force = 0
# system.pendulum.damper
#   - system.pendulum.damper.velocity -> system.pendulum.mass.velocity = 0
#   - system.pendulum.damper.force = 0
# system.gravity
#   - system.gravity.value = 0

class System:
    def __init__(self, name):
        self.name = name

class CompositeSystem(System):
    def __init__(self, name):
        super(CompositeSystem, self).__init__(name)

