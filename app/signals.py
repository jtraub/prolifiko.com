from django.dispatch import Signal

registration = Signal(providing_args=['user'])

new_goal = Signal(providing_args=['goal'])

step_complete = Signal(providing_args=['step'])
new_step = Signal(providing_args=['step'])
