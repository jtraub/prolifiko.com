import django.dispatch

new_goal = django.dispatch.Signal(providing_args=['goal'])

step_complete = django.dispatch.Signal(providing_args=['step'])
new_step = django.dispatch.Signal(providing_args=['step'])
