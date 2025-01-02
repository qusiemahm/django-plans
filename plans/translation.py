from modeltranslation.translator import translator, TranslationOptions
from plans.models import (
    Plan,
    Pricing,
    Quota,
)

class AdminPlanOptions(TranslationOptions):
    fields = ('name', 'description')  # Specify the fields to translate

translator.register(Plan, AdminPlanOptions)

class AdminPricingOptions(TranslationOptions):
    fields = ('name',)  # Specify the fields to translate

translator.register(Pricing, AdminPricingOptions)

class AdminQuotaOptions(TranslationOptions):
    fields = ('name', 'unit', 'description')  # Specify the fields to translate

translator.register(Quota, AdminQuotaOptions)