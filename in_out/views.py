from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Money
from datetime import date, datetime
from time import time
import json
from decimal import Decimal
from collections import OrderedDict
from .fusioncharts import FusionCharts
import simplejson as json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from operator import itemgetter


dataSource = OrderedDict()

# The data for the chart should be in an array wherein each element of the array  is a JSON object having the `label` and `value` as keys.


# Create your views here.

@login_required(login_url='login')
def index(request):


    # Variaveis gerais
    today = date.today()
    today_text = today.strftime('%d/%m/%Y')
    today_text_mY = today.strftime('%m/%Y')
    user = request.user
    # Valor Geral - Cards no topo da tela
    overall_cards_data = get_overall_cards_data(user)
    total_income = overall_cards_data[0]
    total_outcome = overall_cards_data[1]
    balance = overall_cards_data[2]
    # Valores Mensais - grafico de barras
    month_values = get_month_values(user, today.month, today.year)
    total_income_month = month_values[0]
    total_outcome_month = month_values[1]
    balance_month = month_values[2]
    data0 = month_values[3]
    # Valores anuais - grafico pie2d
    year_values = get_value_year(today.year, user)
    year_income = year_values[0]
    year_outcome = year_values[1]
    year_balance = year_income - year_outcome
    data1 = year_values[2]
    # Grafico Gasto mensal
    dataSource = OrderedDict()
    chartConfig = OrderedDict()
    chartConfig["palettecolors"] = "5d62b5,29c3be,f2726f,ff8000,990099,00ffff"
    chartConfig["caption"] = "Gasto mensal"
    chartConfig["subCaption"] = "{}/{}".format(today.month, today.year)
    chartConfig["xAxisName"] = "Categorias"
    chartConfig["yAxisName"] = "Dinheiro gasto (R$)"
    chartConfig["numberSuffix"] = " "
    chartConfig["theme"] = "fusion"
    dataSource["chart"] = chartConfig
    dataSource["data"] = []
    for k, v in data0:
        dataSource["data"].append({"label": k, "value": float(v)})
    dataSource["data"] = sorted(
        dataSource["data"], key=lambda k: k['value'], reverse=True)
    # end
    # Grafico ano atual--
    dataSource1 = OrderedDict()
    chartConfig1 = OrderedDict()
    chartConfig1["palettecolors"] = "5d62b5,29c3be,f2726f,ff8000,990099,00ffff"
    chartConfig1["caption"] = "Gasto ano atual"
    chartConfig1["subCaption"] = "{}".format(today.year)
    chartConfig1["xAxisName"] = "Categorias"
    chartConfig1["yAxisName"] = "Dinheiro gasto (R$)"
    chartConfig1["numberSuffix"] = " "
    chartConfig1["theme"] = "fusion"
    dataSource1["chart"] = chartConfig1
    dataSource1["data"] = []
    for k, v in data1:
        dataSource1["data"].append({"label": k, "value": float(v)})
    dataSource1["data"] = sorted(
        dataSource1["data"], key=lambda k: k['value'], reverse=True)
    # End
    # Chart renders
    column2D = FusionCharts("column2d", "myFirstChart", "600",
                            "500", "myFirstchart-container", "json", dataSource)
    pie2d = FusionCharts("column2d", "sec", "600", "500",
                        "sec-container", "json", dataSource1)
    # End
    # Context
    if request.is_ajax():
        start_date = request.GET.get('date')
        end_date = request.GET.get('date1')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        card_data = []
        #chart data
        queryset0 = Money.objects.values_list(
            'category', 'valor').filter(add_or_remove=True, user=user,entry_date__range=(start_date, end_date))
        queryset = Money.objects.values_list(
            'category', 'valor').filter(add_or_remove=False, user=user,entry_date__range=(start_date, end_date))
        cat_list = ['Trabalho', 'Lazer',
                'Aluguel', 'Gastos Pessoais', 'Investimentos', 'Outro']
        
        val_list = []
        total_outro = 00.00
        total_categoria = Decimal(total_outro)
        for l in range(len(cat_list)):
            tes = 0
            categoria = cat_list[l]
            for i in range(len(queryset)):
                if queryset[i][0] == categoria:
                    tes += queryset[i][1]
            val_list.append(tes)
            
        data2 = list(zip(cat_list, val_list))
        
        soma_out = 0
        for valor in val_list:
            soma_out += valor
        

        val_list0 = []
        for i in range(len(cat_list)):
            tes = 0
            categoria = cat_list[i]
            for i in range(len(queryset0)):
                if queryset0[i][0] == categoria:
                    tes += queryset0[i][1]
            val_list0.append(tes)
        data3 = list(zip(cat_list, val_list0))
        
        
        soma_in = 0
        for valor in val_list0:
            soma_in += valor
        
        balance = soma_in - soma_out
        card_data.append(soma_in)
        card_data.append(soma_out)
        card_data.append(balance)
        

        #chart outcome
        dataSource2 = OrderedDict()
        chartConfig2 = OrderedDict()
        chartConfig2["palettecolors"] = "e60b0b,0be60b"
        chartConfig2["caption"] = "Gasto por categoria: {}/{}/{} - {}/{}/{}".format(start_date.day ,start_date.month, start_date.year, end_date.day,end_date.month, end_date.year)
        chartConfig2["subCaption"] = "{}".format(today.year)
        chartConfig2["xAxisName"] = "Categorias"
        chartConfig2["yAxisName"] = "Dinheiro gasto (R$)"
        chartConfig2["numberSuffix"] = " "
        chartConfig2["theme"] = "fusion"
        dataSource2["chart"] = chartConfig2
        dataSource2["data"] = []
        for k, v in data2:
            dataSource2["data"].append(float(v))



        #chart income
        dataSource3 = OrderedDict()
        chartConfig3 = OrderedDict()
        chartConfig3["palettecolors"] = "e60b0b,0be60b"
        chartConfig3["caption"] = "Gasto por categoria: {}/{}/{} - {}/{}/{}".format(start_date.day ,start_date.month, start_date.year, end_date.day,end_date.month, end_date.year)
        chartConfig3["subCaption"] = "{}".format(today.year)
        chartConfig3["xAxisName"] = "Categorias"
        chartConfig3["yAxisName"] = "Dinheiro gasto (R$)"
        chartConfig3["numberSuffix"] = " "
        chartConfig3["theme"] = "fusion"
        dataSource3["chart"] = chartConfig3
        dataSource3["category"] = cat_list
        dataSource3["data"] = []
        for k, v in data3:
            dataSource3["data"].append(float(v))


        table_query = get_table_row_data(user, start_date, end_date)
        table_data = table_query
        table_data = list(table_data)
        
        


        return JsonResponse({"data": dataSource2, "card": card_data, "data_in": dataSource3, "tabledata": table_data}, safe=False, status=200)

    data = {
        'total_income_month': total_income_month,
        'total_outcome_month': total_outcome_month,
        'balance_month': balance_month,
        'total_income': total_income,
        'total_outcome': total_outcome,
        'balance': balance,
        'data0': data0,
        'output2': pie2d.render(),
        'output': column2D.render(),
        'date': today_text_mY,
        'date_year': today.year,
        'year_income': year_income,
        'year_outcome': year_outcome,
        'year_balance': year_balance,
        'data1': data1,
        
    }
    
    return render(request, 'index.html', data)


def edit(request):
    if request.method == "GET":
        if request.is_ajax():
            user = request.user
            data = request.GET.get('start_date')
            data1 = request.GET.get('end_date')
            start_date = datetime.strptime(data, '%Y-%m-%d')
            end_date = datetime.strptime(data1, '%Y-%m-%d')
            
            
            
            edit_table_data = list(get_table_row_data(user, start_date, end_date))
            
            return JsonResponse({'tabledata': edit_table_data})
        return render(request, 'edit.html')
    else:
        user = request.user

        entry_id = request.POST['entry_id']
        tipo = request.POST['tipo']
        valor = request.POST['valor']
        date = request.POST['date']
        payment = request.POST['payment']
        category = request.POST['category']
        obs = request.POST['obs']
        delete = request.POST['delete']
        
        if tipo == "Entrada":
            tipo = True
        else:
            tipo = False
        money_obj = Money.objects.get(pk = entry_id, user=user)
        if delete == "True":
            money_obj.delete()
        else:
            money_obj.valor = valor
            money_obj.entry_date = date
            money_obj.add_or_remove = tipo
            money_obj.category = category
            money_obj.obs = obs
            money_obj.payment_type = payment
            money_obj.save()

        return render(request, 'edit.html')


def add(request):
    """ Gera uma entrada no banco de dados atreavez de um form """
    if request.method == "POST":
        tipo = request.POST["tipo"]
        valor = "{:.2f}".format(float(request.POST["valor"]))
        date = request.POST["date"]
        payment = request.POST["payment"]
        category = request.POST["category"]
        obs = request.POST["obs"]
        

        if tipo == "Entrada":
            tipo = True
        else:
            tipo = False

        user = get_object_or_404(User, pk=request.user.id)

        money = Money.objects.create(
            user=user,
            valor=valor,
            entry_date=date,
            add_or_remove=tipo,
            payment_type=payment,
            category=category,
            obs = obs
        )
        money.save()
        
        return render(request, 'add.html')
    else:
        return render(request, 'add.html')


def get_value_year(year, user):
    """ Calcula income e outcome anual + gera data apra o grafico 2 (anual)  """
    year_list_income = Money.objects.values_list('valor', flat=True).filter(
        add_or_remove=True, user=user, entry_date__year=year)
    year_income = sum(year_list_income)
    year_list_outcome = Money.objects.values_list('valor', flat=True).filter(
        add_or_remove=False, entry_date__year=year, user=user)
    year_outcome = sum(year_list_outcome)
    queryset_year = list(Money.objects.values('category', 'valor').filter(
        add_or_remove=False, entry_date__year=year, user=user))
    cat_list = ['Outro', 'Trabalho', 'Lazer',
                'Aluguel', 'Gastos Pessoais', 'Investimentos']
    val_list = []
    total_outro = 00.00
    total_categoria = Decimal(total_outro)
    for l in range(len(cat_list)):
        tes = 0
        categoria = cat_list[l]
        for i in range(len(queryset_year)):
            if queryset_year[i]['category'] == categoria:
                tes += queryset_year[i]['valor']
        val_list.append(tes)
    data1 = list(zip(cat_list, val_list))
    return year_income, year_outcome, data1


def get_month_values(user, month, year):
    """ Valores mensais """
    sep_income_month = Money.objects.values_list('valor', flat=True).filter(
        add_or_remove=True, entry_date__month=month, entry_date__year=year, user=user)
    total_income_month = sum(sep_income_month)
    sep_outcome_month = Money.objects.values_list('valor', flat=True).filter(
        add_or_remove=False, entry_date__month=month, entry_date__year=year, user=user)
    total_outcome_month = sum(sep_outcome_month)
    balance_month = total_income_month - total_outcome_month
    queryset = list(Money.objects.values('category', 'valor').filter(
        add_or_remove=False, entry_date__month=month, entry_date__year=year, user=user))
    cat_list = ['Outro', 'Trabalho', 'Lazer',
                'Aluguel', 'Gastos Pessoais', 'Investimentos']
    val_list = []
    total_outro = 00.00
    total_categoria = Decimal(total_outro)
    for l in range(len(cat_list)):
        tes = 0
        categoria = cat_list[l]
        for i in range(len(queryset)):
            if queryset[i]['category'] == categoria:
                tes += queryset[i]['valor']
        val_list.append(tes)
    data0 = list(zip(cat_list, val_list))
    return total_income_month, total_outcome_month, balance_month, data0


def get_overall_cards_data(user):
    sep_total_income = Money.objects.values_list(
        'valor', flat=True).filter(add_or_remove=True, user=user)
    total_income = sum(sep_total_income)
    sep_total_outcome = Money.objects.values_list(
        'valor', flat=True).filter(add_or_remove=False, user=user)
    total_outcome = sum(sep_total_outcome)
    balance = total_income - total_outcome
    return total_income, total_outcome, balance

def get_table_row_data(user, start_date, end_date):
    table_query = Money.objects.values_list(
            'category', 'valor', 'obs', 'entry_date', 'add_or_remove', 'id', 'payment_type').filter(user=user, entry_date__range=(start_date, end_date)).order_by('-entry_date')
    
    return table_query

