from django.http import HttpResponse
from django.shortcuts import render
from .forms import InputNum_Form
from .models import Num, Error_log


def increment(request):
    if request.method == 'POST':
        nf = InputNum_Form(request.POST)
        if nf.is_valid():
            num = nf.cleaned_data['input_num_form']
            for used_num in Num.objects.all():
                if num == used_num.num:
                    er = Error_log(err='Error_1', number=used_num)
                    er.save()
                    output_str = 'Число {} уже обрабатывалось ранее'.format(num)
                    return render(request, 'incrementer/increment.html', {'output_str': output_str, 'form': nf})
                elif num + 1 == used_num.num:
                    er = Error_log(err='Error_2', number=used_num)
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