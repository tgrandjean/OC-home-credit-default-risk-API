from django.db import models

class Application(models.Model):
    """Application."""
    REVOLVING = 'Revolving loans'
    CASH_LOAN = 'Cash loans'

    NAME_CONTRACT_TYPE_CHOICES = [
        (REVOLVING, 'Revolving'),
        (CASH_LOAN, 'Cash')
    ]

    sk_id_curr = models.IntegerField(primary_key=True, unique=True)
    days_birth = models.FloatField(help_text='Age of the appliant')
    occupation_type = models.CharField(max_length=60)
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
