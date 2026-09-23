from .paymentView import PaymentView
from .paymentWebhookView import PaymentWebhookView




'''
payments/
│
├── migrations/
│   └── __init__.py
│
├── models/
│   ├── __init__.py
│   ├── payment.py
│   └── paymentAttempt.py
│
├── serializers/
│   ├── __init__.py
│   └── paymentSerializer.py
│
├── services/
│   ├── __init__.py
│   │
│   ├── paymentService.py
│   ├── paymentVerificationService.py
│   │
│   └── providers/
│       ├── __init__.py
│       ├── onlinePaymentService.py
│       │
│       ├── codPaymentService.py
│       ├── providerAPaymentService.py
│       └── providerBPaymentService.py
│
├── views/
│   ├── __init__.py
│   ├── paymentView.py
│   └── paymentWebhookView.py
│
├── tasks/
│   ├── __init__.py
│   └── paymentReconciliationTask.py
│
├── admin.py
├── apps.py
├── tests.py
├── urls.py
└── __init__.py
'''
