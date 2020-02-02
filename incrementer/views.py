from django.http import HttpResponse
from .models import Num, Error_log


def increment(request, num):
    try:
        num = int(num)
        for used_num in Num.objects.all():
            if num == used_num.num:
                er = Error_log(err='Error_1', number=used_num)
                er.save()
                return HttpResponse('Число {} уже обрабатывалось ранее'.format(num))
            elif num + 1 == used_num.num:
                er = Error_log(err='Error_2', number=used_num)
                er.save()
                return HttpResponse('Число {} на 1 меньше обработанного ранее числа'.format(num))

        used_num = Num(num=num)
        used_num.save()
        return HttpResponse('Обработанное число = {}'.format(num + 1))
    except ValueError:
        return HttpResponse('Запрос не натуральное число!!!')


def clear_db(request):
    for t in Num.objects.all():
        t.delete()
    return HttpResponse('Записи в базе данных удалены')