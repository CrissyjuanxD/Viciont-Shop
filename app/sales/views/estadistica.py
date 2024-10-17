from django.http import JsonResponse
from django.shortcuts import render
from app.sales.models import Invoice, InvoiceDetail
from django.db.models import Sum
from django.utils import timezone
import datetime

def estadisticas_venta(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            
            if start_date and end_date:
                start_date = timezone.make_aware(datetime.datetime.strptime(start_date, '%Y-%m-%d'))
                end_date = timezone.make_aware(datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1) - datetime.timedelta(seconds=1))
                
                # Obtener facturas en el rango de fechas
                invoices = Invoice.objects.filter(issue_date__range=[start_date, end_date])
            else:
                invoices = Invoice.objects.all()

            # Obtener el total de ventas por fecha
            sales_data = invoices.values('issue_date').annotate(
                total_sales=Sum('total')
            ).order_by('issue_date')

            sales_data_list = list(sales_data)

            for item in sales_data_list:
                item['issue_date'] = item['issue_date'].isoformat()

            return JsonResponse(sales_data_list, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return render(request, 'components/homepro.html', {
            'title1': 'Estadísticas de Ventas',
            'title2': 'Ventas por Fecha'
        })