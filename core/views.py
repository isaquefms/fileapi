import time
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import File, Billing
from core.utils import CreatePDFBillingClient, SendNotificationBillingClient, create_default_api_response, log_info, read_csv_file
            

def process_csv_content(file, file_id: int) -> list:
    """Função para processar o conteúdo de um arquivo csv.
    
    Args:
        file (File): Arquivo csv a ser processado.
        file (int): Id do arquivo para registro.
    
    Returns:
        list: Lista com os objetos criados durante a leitura.
    """
    et1 = time.time()
    bills = [Billing(file_id=file_id,
                     name=row.get('name'),
                     government_id=row.get('governmentId'),
                     email=row.get('email'),
                     debt_amount=row.get('debtAmount'),
                     debt_due_date=row.get('debtDueDate'),
                     debt_id=row.get('debtId')) for row in read_csv_file(file)]
    et2 = time.time()
    log_info(f'Processamento do arquivo: {et2 - et1}')
    Billing.objects.bulk_create(bills, ignore_conflicts=True)
    log_info(f'Inserção no banco: {time.time() - et2}')
    

def send_notification(billing: Billing):
    """Função para enviar uma notificação para o usuário.
    
    Args:
        billing (Billing): Cobrança a ser notificada.
    """
    client = SendNotificationBillingClient()
    return client.send_notification(billing)


def create_pdf_file(billing: Billing):
    """Função para criar um arquivo pdf com os dados da cobrança.
    
    Args:
        billing (Billing): Cobrança a ser notificada.
    """
    client = CreatePDFBillingClient()
    return client.create_pdf_file(billing)


def send_notification_and_create_pdf(file_id: int):
    """Função para enviar uma notificação e criar um arquivo pdf com os dados da cobrança.
    
    Args:
        file_id (int): ID do arquivo criado.
    """
    objs = Billing.objects.filter(file_id=file_id)
    for billing in objs:
        create_pdf_file(billing)
        send_notification(billing)
    objs.update(status=Billing.Status.NOTIFICATION_SENT)
    

async def process_file(request):
    if request.method != 'POST':
        return JsonResponse(create_default_api_response(405, 'method not allowed', 'method not allowed'), status=405)
    
    uploaded_file = request.FILES['file']
    filename = uploaded_file.name
    
    # validando se o arquivo é um csv
    if not filename.endswith('.csv'):
        return HttpResponse(create_default_api_response(400, 'file received with error', 'file must be a csv'), status=400)
    
    file = File.objects.create(file=uploaded_file)
    process_csv_content(file.file.path, file.id)
    send_notification_and_create_pdf(file.id)
    return HttpResponse(create_default_api_response(201, 'file received', 'created'), status=201)
