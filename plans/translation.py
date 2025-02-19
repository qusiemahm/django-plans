from modeltranslation.translator import translator, TranslationOptions
from plans.models import (
    Plan,
    Pricing,
    Quota,
)
from plans.base.models import UserPlanCancellationReason


class AdminPlanOptions(TranslationOptions):
    fields = ("name", "description")  # Specify the fields to translate


translator.register(Plan, AdminPlanOptions)


class AdminPricingOptions(TranslationOptions):
    fields = ("name",)  # Specify the fields to translate


translator.register(Pricing, AdminPricingOptions)


class AdminQuotaOptions(TranslationOptions):
    fields = ("name", "unit", "description")  # Specify the fields to translate


translator.register(Quota, AdminQuotaOptions)


class AdminUserPlanCancellationReason(TranslationOptions):
    fields = ("reason",)  # Specify the fields to translate


translator.register(UserPlanCancellationReason, AdminUserPlanCancellationReason)
