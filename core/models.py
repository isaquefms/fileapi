from django.db import models

from .utils import BaseModel, get_unique_file_path, validate_file_extension


class File(BaseModel):
    """Modelo para armazenar arquivos.
    """
    
    # O validator garante que apenas arquivos csv sejam aceitos. Isso evita que erros no método de leitura sejam
    #   causados por arquivos com extensões diferentes.
    file = models.FileField(upload_to=get_unique_file_path, validators=[validate_file_extension])
    
    # Não é necessário ter o modelo em sí, porém podemos escolher essa abordagem para se ter um registro
    #   de todos os arquivos enviados.
    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return self.file.name


class Billing(BaseModel):
    """Modelo para armazenar as informações de cobrança.
    """
    
    # Pretendemos usar os status para controlar a cobrança dentro do sistema.
    class Status(models.TextChoices):
        PENDING = 'PE', 'PENDING' 
        INVOICE_CREATED =  'IC', 'INVOICE CREATED'
        NOTIFICATION_SENT =  'NS', 'NOTIFICATION SENT'
    
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    government_id = models.CharField(max_length=50)
    email = models.EmailField()
    debt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debt_due_date = models.DateField()
    # O campo debt_id é um campo único, ou seja, não pode haver dois registros com o mesmo valor.
    #   Isso é importante para garantir que não haja duplicidade de registros de cobrança mesmo que haja linhas
    #   repetidas ou se um arquivo for processado pela metade.
    debt_id = models.UUIDField(unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)

    class Meta:
        verbose_name = 'Billing'
        verbose_name_plural = 'Billings'

    def __str__(self):
        return self.status