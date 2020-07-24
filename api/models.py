from django.db import models

class Application(models.Model):
    """Application."""
    REVOLVING = 'Revolving loans'
    CASH_LOAN = 'Cash loans'

    NAME_CONTRACT_TYPE_CHOICES = [
        (REVOLVING, 'Revolving'),
        (CASH_LOAN, 'Cash')
    ]

    OCCUPATION_TYPE_CHOICES = [('Laborers', 'Laborers'),
                               ('Core staff', 'Core staff'),
                               ('Accountants', 'Accountants'),
                               ('Managers', 'Managers'),
                               ('unknown', 'unknown'),
                               ('Drivers', 'Drivers'),
                               ('Sales staff', 'Sales staff'),
                               ('Cleaning staff', 'Cleaning staff'),
                               ('Cooking staff', 'Cooking staff'),
                               ('Private service staff', 'Private service staff'),
                               ('Medicine staff', 'Medicine staff'),
                               ('Security staff', 'Security staff'),
                               ('High skill tech staff', 'High skill tech staff'),
                               ('Waiters/barmen staff', 'Waiters/barmen staff'),
                               ('Low-skill Laborers', 'Low-skill Laborers'),
                               ('Realty agents', 'Realty agents'),
                               ('Secretaries', 'Secretaries'),
                               ('IT staff', 'IT staff'),
                               ('HR staff', 'HR staff')]

    sk_id_curr = models.IntegerField(primary_key=True, unique=True)
    days_birth = models.FloatField(help_text='Age of the appliant')
    occupation_type = models.CharField(max_length=60,
                                       choices=OCCUPATION_TYPE_CHOICES)
    amt_income_total = models.FloatField(help_text='Total income of the appliant')
    amt_credit = models.FloatField()
    name_contract_type = models.CharField(max_length=16,
                                          choices=NAME_CONTRACT_TYPE_CHOICES,
                                          default=CASH_LOAN)
    amt_annuity = models.FloatField()
    ext_source_1 = models.FloatField(null=True)
    ext_source_2 = models.FloatField(null=True)
    ext_source_3 = models.FloatField(null=True)
    total_prev_hc = models.IntegerField()
    credit_active_closed = models.IntegerField()
    credit_active_active = models.IntegerField()
    active_cred_hc = models.IntegerField()
    bad_payment_hc = models.IntegerField()
    reported_dpd = models.IntegerField(default=0)
