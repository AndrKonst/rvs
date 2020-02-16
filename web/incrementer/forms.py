from django import forms

class InputNum_Form(forms.Form):
    input_num_form = forms.IntegerField(label='Введите число')