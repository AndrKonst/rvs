from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import F
from .forms import InputNum_Form
from .models import Num, Error_log


def increment(request):
    if request.method == 'POST':
        nf = InputNum_Form(request.POST)
        if nf.is_valid():
            num = nf.cleaned_data['input_num_form']
            if num < 0:
                output_str = 'Число {} меньше 0. Введите натуральное число'.format(num)
                return render(request, 'incrementer/increment.html', {'output_str': output_str, 'form': nf})
            num_from_db = Num.objects.values('num', num_minus_1=F('num') - 1)
            if num_from_db.exists():
                for used_num in num_from_db:
                    if used_num['num'] == num:
                        er = Error_log(err='Error_1', number=Num.objects.get(num=num))
                        er.save()
                        output_str = 'Число {} уже обрабатывалось ранее'.format(num)
                        return render(request, 'incrementer/increment.html', {'output_str': output_str, 'form': nf})
                    elif used_num['num_minus_1'] == num:
                        er = Error_log(err='Error_2', number=Num.objects.get(num=num + 1))
                        er.save()
                        output_str = 'Число {} на 1 меньше обработанного ранее числа'.format(num)
                        return render(request, 'incrementer/increment.html', {'output_str': output_str, 'form': nf})
            used_num = Num(num=num)
            used_num.save()
            output_str = 'Обработанное число = {}'.format(num + 1)
            return render(request, 'incrementer/increment.html', {'output_str': output_str, 'form': nf})
    else:
        nf = InputNum_Form()
        return render(request, 'incrementer/increment.html', {'form': nf})


def clear_db(request):
    for t in Num.objects.all():
        t.delete()
    return HttpResponse('Записи в базе данных удалены')