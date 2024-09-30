import time

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import File, Billing
from core.utils import CreatePDFBillingClient, SendNotificationBillingClient, create_default_api_response, log_debug, log_error, log_info, read_csv_file
from .serializers import FileSerializer, BillingSerializer
            

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


# As views poderiam ser feitas via method_based porém achei melhor usar o Rest Framework para facilitar a implementação.
class FileViewSet(ViewSet):
    """Definição da viewset para o modelo File.
    """
    
    serializer_class = FileSerializer
    
    def list(self, request):
        return Response({'detail': 'Method not allowed'}, status=405)
    
    def create(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            process_csv_content(file.file.path, file.id)
            send_notification_and_create_pdf(file.id)
            return Response(create_default_api_response(201, 'file received', serializer.data), status=201)
        return Response(create_default_api_response(400, 'file received with error', serializer.errors), status=400)