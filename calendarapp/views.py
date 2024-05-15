from django.shortcuts import render
from .calendarific import get_holidays

def holidays_view(request):
    api_key = 'Hy4WtcGev8f5sBuYNA96vFxD0HQy1ln3'
    country = 'CO'
    year = 2024
    language = request.GET.get('language', 'es')
    holidays = get_holidays(api_key, country, year, language)
    return render(request, 'calendarapp/holidays.html', {'holidays': holidays})