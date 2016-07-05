from django.shortcuts import render


def about(request):
    return render(request, 'menu/about.html')


def terms(request):
    return render(request, 'menu/terms.html')


def privacy(request):
    return render(request, 'menu/privacy.html')


def help(request):
    return render(request, 'menu/help.html')
