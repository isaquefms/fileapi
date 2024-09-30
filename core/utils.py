import os
import csv
from typing import Generator
import uuid
import logging

from django.db import models
from django.core.exceptions import ValidationError


def get_unique_file_path(instance, filename):
    """Função para definir o caminho único do arquivo usando uuid.
    
    Args:
        instance (File): Instância do arquivo.
        filename (str): Nome do arquivo.
    
    Returns:
        str: Caminho do arquivo.
    """
    # ref: https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('files', filename)


def validate_file_extension(value):
    """Função para validar a extensão do arquivo.
    
    Args:
        value (File): Arquivo a ser validado.
    
    Raises:
        ValidationError: Caso a extensão do arquivo não seja .csv.
    """
    if not value.name.endswith('.csv'):
        raise ValidationError('Invalid file extension. Only .csv files are allowed.')
    
    
def create_default_api_response(status: int, message: str, data: dict = None):
    """Função para criar uma resposta padrão para a API.
    
    Args:
        status (int): Status da resposta.
        message (str): Mensagem da resposta.
        data (dict): Dados da resposta.
    
    Returns:
        dict: Resposta da API.
    """
    return {
        'status': status,
        'message': message,
        'data': data
    }
    
    
# Métodos para logar em cada um dos loggers criados no settings.py
def log_debug(message: str):
    """Função para logar mensagens de debug.

    Args:
        message (str): Mensagem a ser logada.
    """
    logger = logging.getLogger('debug')
    logger.exception(message)    


def log_error(message: str):
    """Função para logar mensagens de erro.

    Args:
        message (str): Mensagem a ser logada.
    """
    logger = logging.getLogger('django')
    logger.error(message)
    
    
def log_info(message: str):
    """Função para logar mensagens de informação.
    
    Args:
        message (str): Mensagem a ser logada.
    """
    logger = logging.getLogger('processing')
    logger.info(message)


def read_csv_file(file) -> Generator:
    """Função para ler um arquivo csv e retornar uma lista de dicionários.
    
    Args:
        file (File): Arquivo csv a ser lido.
    
    Returns:
        list: generator de dicionários com os dados do arquivo.
    """
    with open(file, 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            yield row
            
            
def default_processing() -> bool:
    """Função para simular um processamento.
    
    Returns:
        bool: Resultado do processamento.
    """
    return True


class DefaultProcessing():
    """Classe para simular um processamento aleatório com 90% de taxa de sucesso.
    """
    
    # Método para verificar o funcionamento do serviço. Utilizado para teste de integração.
    def check_service(self) -> bool:
        return True
    
    def process(self) -> bool:
        return default_processing()


class CreatePDFBillingClient(DefaultProcessing):
    """Classe para criar um arquivo pdf com os dados da cobrança.
    """
    
    def create_pdf_file(self, billing) -> bool:
        """Função para criar um arquivo pdf com os dados da cobrança.
        
        Args:
            billing (Billing): Cobrança a ser criada.
            
        Returns:
            bool: Resultado do processamento.
        """
        if self.process():
            log_info(f'Creating pdf file for billing {billing.debt_id}')
            return True
        log_info(f'Error creating pdf file for billing {billing.debt_id}')
        return False
    
    
class SendNotificationBillingClient(DefaultProcessing):
    """Classe para enviar uma notificação para o usuário.
    """
    
    def send_notification(self, billing) -> bool:
        """Função para enviar uma notificação para o usuário.
        
        Args:
            billing (Billing): Cobrança a ser notificada.
            
        Returns:
            bool: Resultado do processamento.
        """
        if self.process():
            log_info(f'Sending notification for billing {billing.debt_id}')
            return True
        log_info(f'Error sending notification for billing {billing.debt_id}')
        return False
            

class BaseModel(models.Model):
    """Base model para todos os modelos do projeto conterem created_at e updated_at.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
