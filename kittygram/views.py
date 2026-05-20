from django.contrib.auth import get_user_model
from django.shortcuts import render

from cats.models import Cat
from health.models import Clinic, HealthRecord

User = get_user_model()


def index(request):
    context = {
        'cats_count': Cat.objects.count(),
        'users_count': User.objects.count(),
        'records_count': HealthRecord.objects.count(),
        'clinics_count': Clinic.objects.count(),
    }
    return render(request, 'index.html', context)
