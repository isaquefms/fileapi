from django.test import TestCase, Client


class TestApiCall(TestCase):
    
    def test_file_submission(self):
        client = Client()
        
        # enviando o arquivo csv para a api
        response = client.post('/api/files/', {'file': 'test.txt'})
        assert response.status_code == 201
        assert response.json() == {'file': 'test.txt'}
    
    
    