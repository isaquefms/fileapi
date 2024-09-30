from django.test import TestCase, Client

from core.models import Billing, File
from core.utils import CreatePDFBillingClient, DefaultProcessing, SendNotificationBillingClient, create_default_api_response, default_processing, get_unique_file_path, validate_file_extension


class ApiUnitTests(TestCase):
    
    def setUp(self) -> None:
        self.billing = Billing(
            file=File(file="test.csv"),
            name="Test",
            government_id="123456789",
            email="email@email.com",
            debt_amount=10.00,
            debt_due_date="2021-01-01",
            debt_id="123e4567-e89b-12d3-a456-426614174000",
            status="PE",
        )

    def test_file_model(self):
        file = File(file="test.csv")
        self.assertEqual(file.__str__(), "test.csv")

    def test_billing_model(self):
        self.assertEqual(self.billing.__str__(), "PE")
        self.assertEqual(self.billing.status, "PE")
        self.assertEqual(self.billing.file.__str__(), "test.csv")
        self.assertEqual(self.billing.name, "Test")
        self.assertEqual(self.billing.government_id, "123456789")
        self.assertEqual(self.billing.email, "email@email.com")
        self.assertEqual(self.billing.debt_amount, 10.00)
        self.assertEqual(self.billing.debt_due_date, "2021-01-01")
        self.assertEqual(self.billing.debt_id, "123e4567-e89b-12d3-a456-426614174000")

    def test_get_unique_file_path(self):
        file_path = get_unique_file_path("instance", "filename.csv")
        # o método deve garantir que o caminho do arquivo seja diferente do caminho padrão
        self.assertNotEqual(file_path, "files/filename.csv")
        
    def test_validate_file_extension(self):
        file = File(file="test.txt")
        with self.assertRaises(Exception) as context:
            validate_file_extension(file.file)
        self.assertTrue("Invalid file extension. Only .csv files are allowed." in str(context.exception))
        
    def test_validate_file_extension_csv(self):
        file = File(file="test.csv")
        self.assertIsNone(validate_file_extension(file.file))
        
    def test_create_default_api_response(self):
        response = create_default_api_response(200, "Test", {"data": "test"})
        self.assertEqual(response, {'status': 200, 'message': 'Test', 'data': {'data': 'test'}})
     
    def test_default_processing(self):
        self.assertEqual(default_processing(), True)
        
    def test_default_processing_class(self):
        obj = DefaultProcessing()
        self.assertEqual(obj.process(), True)

    def test_create_pdf_billing_client(self):
        client = CreatePDFBillingClient()
        self.assertEqual(client.create_pdf_file(self.billing), True)
        
    def test_send_notification_billing_client(self):
        client = SendNotificationBillingClient()
        self.assertEqual(client.send_notification(self.billing), True)

    
class ApiIntegrationTests(TestCase):
    
    def setUp(self) -> None:
        self.client = Client()
        self.email_client = SendNotificationBillingClient()
        self.pdf_client = CreatePDFBillingClient()
        self.file = File(file="test.csv")
        self.file.save()
        self.billing = Billing(
            file=self.file,
            name="Test",
            government_id="123456789",
            email="email@email.com",
            debt_amount=10.00,
            debt_due_date="2021-01-01",
            debt_id="123e4567-e89b-12d3-a456-426614174000",
            status="PE",
        )
    
    def test_api_get_method_not_allowed(self):
        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, 405)
        
    def test_email_client_is_working(self):
        self.assertEqual(self.email_client.check_service(), True)

    def test_pdf_client_is_working(self):
        self.assertEqual(self.pdf_client.process(), True)