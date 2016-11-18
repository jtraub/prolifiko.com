from django.dispatch import Signal

registration = Signal(providing_args=['user'])

new_goal = Signal(providing_args=['goal'])
goal_complete = Signal(providing_args=['goal'])

new_step = Signal(providing_args=['step'])
step_complete = Signal(providing_args=['step'])

email = Signal(providing_args=['email'])
