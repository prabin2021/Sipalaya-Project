from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from unittest.mock import patch, MagicMock

from .models import Payment, PaymentMethod, InstallmentPlan
from courses.models import Course, Enrollment, Category

class PaymentIntegrationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name='Test Category',
            description='A test category'
        )
        
        # Create a test course
        self.course = Course.objects.create(
            title='Test Course',
            price=1000.00,
            description='A test course',
            category=self.category,
            instructor=User.objects.create_user(username='instructor', password='testpass'),
            skill_level='beginner',
            duration='short'
        )
        
        # Create a test payment method
        self.payment_method, _ = PaymentMethod.objects.get_or_create(
            name='test_method', 
            is_active=True
        )
        
        # Set up test client
        self.client = Client()
        self.client.login(username='testuser', password='testpass')


    def test_installment_plan_creation(self):
        # Simulate installment payment
        response = self.client.post(
            reverse('payments:initiate_payment', args=[self.course.id]), 
            {
                'payment_method': 'esewa', 
                'is_installment': 'true', 
                'number_of_installments': '3'
            }
        )
        
        # Check installment plan creation
        installment_plan = InstallmentPlan.objects.filter(
            student=self.user, 
            course=self.course
        ).first()
        
        self.assertIsNotNone(installment_plan)
        self.assertEqual(installment_plan.number_of_installments, 3)
        self.assertEqual(
            installment_plan.amount_per_installment, 
            self.course.price / 3
        )

    @patch('payments.views.requests.get')
    def test_check_payment_status(self, mock_get):
        # Create first payment
        payment = Payment.objects.create(
            student=self.user,
            course=self.course,
            amount=self.course.price / 3,
            payment_method=self.esewa_method,
            transaction_id='test_transaction_uuid',
            is_installment=True,
            installment_number=1,
            total_installments=3
        )
        
        # Mock eSewa status check response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'COMPLETE'}
        mock_get.return_value = mock_response
        
        # Check payment status
        response = self.client.get(
            reverse('payments:check_payment_status', args=['test_transaction_uuid'])
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')

