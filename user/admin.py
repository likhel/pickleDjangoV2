

# Register your models here.



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile, Address, CustomUser,SellerProfile  # Import your models



CustomUser = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0 # Do not show extra blank forms
    verbose_name_plural = 'addresses'

class SellerProfileInline(admin.StackedInline):
        model = SellerProfile
        can_delete = False  # You might want to allow deleting a seller profile
        verbose_name_plural = 'seller profile'
        # Add fields you want to display and edit in the inline
        fields = (
            'business_name',
            'business_type',
            'business_registration_number',
            'tax_identification_number',
            'bank_name',
            'bank_account_number',
            'bank_account_holder_name',
            'business_phone_number',
            'business_email',
            'business_country',
            'business_city',
            'business_street',
            'business_postal_code',
            'shipping_policy',
            'return_policy',
            'is_verified',
        )


class CustomUserAdmin(UserAdmin):
    # inlines = (ProfileInline, AddressInline,SellerProfileInline,) 
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active',) 
    list_filter = ('role', 'is_staff', 'is_active',) 
    search_fields = ('email', 'first_name', 'last_name',) 


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ( 
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2',
                ),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}), # Include 'role' here
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    exclude = ('username',)

    def get_inline_instances(self, request, obj=None):
        """Return inlines conditionally based on role."""
        inlines = [ProfileInline(self.model, self.admin_site), AddressInline(self.model, self.admin_site)]

        if obj and obj.role == "seller":  # Only show SellerProfile for sellers
            inlines.append(SellerProfileInline(self.model, self.admin_site))

        return inlines



admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(SellerProfile) 
