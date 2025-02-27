from copy import deepcopy

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import OrderedModelAdmin

from plans.base.models import (
    AbstractBillingInfo,
    AbstractInvoice,
    AbstractOrder,
    AbstractPlan,
    AbstractPlanPricing,
    AbstractPlanQuota,
    AbstractPricing,
    AbstractQuota,
    AbstractRecurringUserPlan,
    AbstractUserPlan,
    UserPlanCancellationReason,
)

from .signals import account_automatic_renewal
from django.db.models import Count, Q, Min
from django.utils import timezone
from django.conf import settings
from .forms import PlanAdminForm, PricingAdminForm, QuotaAdminForm

Invoice = AbstractInvoice.get_concrete_model()
UserPlan = AbstractUserPlan.get_concrete_model()
Plan = AbstractPlan.get_concrete_model()
PlanQuota = AbstractPlanQuota.get_concrete_model()
Quota = AbstractQuota.get_concrete_model()
PlanPricing = AbstractPlanPricing.get_concrete_model()
Pricing = AbstractPricing.get_concrete_model()
RecurringUserPlan = AbstractRecurringUserPlan.get_concrete_model()
Order = AbstractOrder.get_concrete_model()
BillingInfo = AbstractBillingInfo.get_concrete_model()


class UserPlanCancellationReasonAdmin(admin.ModelAdmin):
    search_fields = ("reason", "description")
    list_display = (
        "reason",
        "description",
        "hidden",
    )
    list_filter = ("hidden",)


class UserLinkMixin(object):
    def user_link(self, obj):
        user_model = get_user_model()
        app_label = user_model._meta.app_label
        model_name = user_model._meta.model_name
        change_url = reverse(
            "admin:%s_%s_change" % (app_label, model_name), args=(obj.user.id,)
        )
        return format_html('<a href="{}">{}</a>', change_url, obj.user.username)

    user_link.short_description = "User"
    user_link.allow_tags = True


class PlanQuotaInline(admin.TabularInline):
    model = PlanQuota

    def has_add_permission(self, request, obj=None):
        # Allow adding only when creating a new plan
        return obj is None

    def has_delete_permission(self, request, obj=None):
        # Allow deletion only when creating a new plan
        return obj is None

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Only make readonly on change form
            return [field.name for field in PlanQuota._meta.fields]
        return []


class PlanPricingInline(admin.TabularInline):
    model = PlanPricing

    def has_add_permission(self, request, obj=None):
        # Allow adding only when creating a new plan
        return obj is None

    def has_delete_permission(self, request, obj=None):
        # Allow deletion only when creating a new plan
        return obj is None

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Only make readonly on change form
            return [field.name for field in PlanPricing._meta.fields]
        return []


class PricingAdmin(admin.ModelAdmin):
    form = PricingAdminForm


class QuotaAdmin(OrderedModelAdmin):
    form = QuotaAdminForm
    list_display = [
        "codename",
        "name",
        "description",
        "unit",
        "is_boolean",
        "move_up_down_links",
    ]

    readonly_fields = ("created", "updated_at")
    list_display_links = list_display


def copy_plan(modeladmin, request, queryset):
    """
    Admin command for duplicating plans preserving quotas and pricings.
    """
    for plan in queryset:
        plan_copy = deepcopy(plan)
        plan_copy.id = None
        plan_copy.available = False
        plan_copy.default = False
        plan_copy.created = None
        plan_copy.save(force_insert=True)

        for pricing in plan.planpricing_set.all():
            pricing.id = None
            pricing.plan = plan_copy
            pricing.save(force_insert=True)

        for quota in plan.planquota_set.all():
            quota.id = None
            quota.plan = plan_copy
            quota.save(force_insert=True)


copy_plan.short_description = _("Make a plan copy")


class PricingRangeFilter(admin.SimpleListFilter):
    title = "Price Range"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        cu = settings.PLANS_CURRENCY
        return (
            ("free", "Free"),
            ("1_300", f"1 {cu} to 300 {cu}"),
            ("301_plus", f"above 300 {cu}"),
        )

    def queryset(self, request, queryset):
        if self.value() == "free":
            return queryset.filter(
                Q(planpricing__price=0) | Q(planpricing__isnull=True)
            ).distinct()
        elif self.value() == "1_300":
            return queryset.filter(
                planpricing__price__gt=0, planpricing__price__lte=300
            ).distinct()
        elif self.value() == "301_plus":
            return queryset.filter(planpricing__price__gt=300).distinct()
        return queryset


class PlanAdmin(OrderedModelAdmin):
    form = PlanAdminForm
    search_fields = (
        "name",
        "customized__username",
        "customized__email",
    )
    list_filter = (
        "available",
        "visible",
        PricingRangeFilter,
    )
    list_display = [
        "name",
        "description",
        "get_price",
        "get_active_subscribers",
        "free_trial_days",
        "visible",
        "available",
        "created",
    ]
    list_display_links = list_display
    inlines = (PlanPricingInline, PlanQuotaInline)
    list_select_related = True
    raw_id_fields = ("customized",)
    readonly_fields = ("created", "updated_at")
    actions = [
        copy_plan,
    ]

    def get_queryset(self, request):
        return (
            super(PlanAdmin, self)
            .get_queryset(request)
            .select_related("customized")
            .prefetch_related("planpricing_set")
            .annotate(
                min_price=Min("planpricing__price"),
                active_subscribers_count=Count(
                    "userplan",
                    filter=Q(userplan__active=True, userplan__expire__isnull=True)
                    | Q(
                        userplan__active=True,
                        userplan__expire__gte=timezone.now().date(),
                    ),
                ),
            )
        )

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:  # Only make readonly on change form
    #         # Get all model fields
    #         all_fields = [field.name for field in self.model._meta.fields]
    #         # Remove 'available' and 'visible' from readonly fields
    #         readonly_fields = [
    #             f for f in all_fields if f not in ("available", "visible", "default")
    #         ]
    #         return readonly_fields
    #     return self.readonly_fields  # Use default readonly_fields for add form

    def get_price(self, obj):
        pricing = obj.planpricing_set.first()
        if pricing:
            return f"{pricing.price} {settings.PLANS_CURRENCY}"
        return "-"

    get_price.short_description = "Pricing"
    get_price.admin_order_field = "min_price"  # Enable sorting by price


    def get_active_subscribers(self, obj):
        return getattr(obj, "active_subscribers_count", 0)

    get_active_subscribers.short_description = "Active Subscribers"
    get_active_subscribers.admin_order_field = (
        "active_subscribers_count"  # Enable sorting by subscriber count
    )

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        fields.remove("name")
        fields.remove("description")
        if obj and obj.plan_for == "vendors":
            fields.remove("price_per_student")
        return fields


class BillingInfoAdmin(UserLinkMixin, admin.ModelAdmin):
    search_fields = ("user__username", "user__email", "tax_number", "name")
    list_display = (
        "user",
        "tax_number",
        "name",
        "street",
        "zipcode",
        "city",
        "country",
    )
    list_display_links = list_display
    list_select_related = True
    readonly_fields = ("user_link", "created", "updated_at")
    exclude = ("user",)


def make_order_completed(modeladmin, request, queryset):
    for order in queryset:
        order.complete_order()


make_order_completed.short_description = _("Make selected orders completed")


def make_order_returned(modeladmin, request, queryset):
    for order in queryset:
        order.return_order()


make_order_returned.short_description = _("Make selected orders returned")


def make_order_invoice(modeladmin, request, queryset):
    for order in queryset:
        if (
            Invoice.objects.filter(
                type=Invoice.INVOICE_TYPES["INVOICE"], order=order
            ).count()
            == 0
        ):
            Invoice.create(order, Invoice.INVOICE_TYPES["INVOICE"])


make_order_invoice.short_description = _("Make invoices for orders")


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    raw_id_fields = ("user",)


class OrderAdmin(admin.ModelAdmin):
    list_filter = ("status", "created", "completed", "plan__name", "pricing")
    raw_id_fields = ("user",)
    search_fields = ("id", "user__username", "user__email", "invoice__full_number")
    list_display = (
        "id",
        "name",
        "created",
        "user",
        "status",
        "completed",
        "tax",
        "amount",
        "get_total_amount",
        "currency",
        "plan",
        "pricing",
        "plan_extended_from",
        "plan_extended_until",
    )
    readonly_fields = ("created", "updated_at", "get_total_amount")
    list_display_links = list_display
    actions = [make_order_completed, make_order_returned, make_order_invoice]
    inlines = (InvoiceInline,)

    def queryset(self, request):
        return (
            super(OrderAdmin, self)
            .queryset(request)
            .select_related("plan", "pricing", "user")
        )

    def get_total_amount(self, obj):
        return obj.total()
    
    get_total_amount.short_description = "Total Amount"
    get_total_amount.admin_order_field = "Total Amount"


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ("full_number", "buyer_tax_number", "user__username", "user__email")
    list_filter = (
        "type",
        "issued",
        "tax",
        "currency",
        "buyer_country",
    )
    list_display = (
        "full_number",
        "issued",
        "total_net",
        "currency",
        "user",
        "tax",
        "buyer_name",
        "buyer_city",
        "buyer_tax_number",
    )
    readonly_fields = ("created", "updated_at")
    list_display_links = list_display
    list_select_related = True
    raw_id_fields = ("user", "order")


class RecurringPlanInline(admin.StackedInline):
    model = RecurringUserPlan
    readonly_fields = ("created", "updated_at")
    extra = 0


def autorenew_payment(modeladmin, request, queryset):
    """
    Automatically renew payment for this plan
    """
    for user_plan in queryset:
        account_automatic_renewal.send(sender=None, user=user_plan.user)


autorenew_payment.short_description = _("Autorenew plan")


class UserPlanAdmin(UserLinkMixin, admin.ModelAdmin):
    list_filter = (
        "active",
        "expire",
        "plan__name",
        "plan__available",
        "plan__visible",
        "recurring__renewal_triggered_by",
        "recurring__payment_provider",
        "recurring__token_verified",
        "recurring__pricing",
    )
    search_fields = ("user__username", "user__email", "plan__name", "recurring__token")
    list_display = (
        "user",
        "plan",
        "branches",
        "expire",
        "active",
        "recurring__renewal_triggered_by",
        "recurring__token_verified",
        "recurring__payment_provider",
        "recurring__pricing",
    )
    list_display_links = list_display
    list_select_related = True
    readonly_fields = ("user_link", "created", "updated_at")
    inlines = (RecurringPlanInline,)
    actions = [
        autorenew_payment,
    ]
    fields = (
        "user",
        "user_link",
        "plan",
        "branches",
        "students",
        "expire",
        "active",
        "paid",
        "canceled_date",
        "cancellation_reason",
        "activated_date",
        "trial_start_date",
        "trial_end_date",
        "created",
        "updated_at",
    )
    raw_id_fields = [
        "user",
        "plan",
    ]

    def recurring__renewal_triggered_by(self, obj):
        return obj.recurring.renewal_triggered_by

    recurring__renewal_triggered_by.admin_order_field = (
        "recurring__renewal_triggered_by"
    )
    recurring__renewal_triggered_by.short_description = "Renewal triggered by"

    def recurring__token_verified(self, obj):
        return obj.recurring.token_verified

    recurring__token_verified.admin_order_field = "recurring__token_verified"
    recurring__token_verified.boolean = True
    recurring__token_verified.short_description = "Renewal token verified"

    def recurring__payment_provider(self, obj):
        return obj.recurring.payment_provider

    recurring__payment_provider.admin_order_field = "recurring__payment_provider"
    recurring__payment_provider.short_description = "Renewal payment_provider"

    def recurring__pricing(self, obj):
        return obj.recurring.pricing

    recurring__pricing.admin_order_field = "recurring__pricing"

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if obj and obj.plan.plan_for == "vendors":
            fields.remove("students")
        return fields


admin.site.register(Quota, QuotaAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(UserPlan, UserPlanAdmin)
admin.site.register(Pricing, PricingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingInfo, BillingInfoAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(UserPlanCancellationReason, UserPlanCancellationReasonAdmin)
