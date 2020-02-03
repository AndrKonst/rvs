from django.http import HttpResponse
from django.template import loader
from .models import Num, Error_log


def increment(request, num):
    template = loader.get_template('incrementer/increment.html')
    try:
        num = int(num)
        for used_num in Num.objects.all():
            if num == used_num.num:
                er = Error_log(err='Error_1', number=used_num)
                er.save()
                output_str = 'Число {} уже обрабатывалось ранее'.format(num)
                context = {'output_str': output_str}
                return HttpResponse(template.render(context, request))
            elif num + 1 == used_num.num:
                er = Error_log(err='Error_2', number=used_num)
                er.save()
                output_str = 'Число {} на 1 меньше обработанного ранее числа'.format(num)
                context = {'output_str': output_str}
                return HttpResponse(template.render(context, request))

        used_num = Num(num=num)
        used_num.save()
        output_str = 'Обработанное число = {}'.format(num + 1)
        context = {'output_str': output_str}
        return HttpResponse(template.render(context, request))
    except ValueError:
        output_str = 'Запрос не натуральное число!!!'
        context = {'output_str': output_str}
        return HttpResponse(template.render(context, request))


def clear_db(request):
    for t in Num.objects.all():
        t.delete()
    return HttpResponse('Записи в базе данных удалены')