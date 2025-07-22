

# Register your models here.



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile, Address, CustomUser,SellerProfile  # Import your models


# Get the custom user model
CustomUser = get_user_model()

# Define an Inline for the Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define an Inline for the Address model
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

# Define a Custom User Admin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, AddressInline,SellerProfileInline,) # Add Profile and Address inlines
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active',) # Add 'role' to list display
    list_filter = ('role', 'is_staff', 'is_active',) # Add 'role' to list filter
    search_fields = ('email', 'first_name', 'last_name',) # Add search fields

    # Add 'role' to the fieldsets for editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}), # Include 'role' here
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ( # Fieldsets for adding a new user
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}), # Include 'role' here
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


# Register your models with the custom admin classes
admin.site.register(CustomUser, CustomUserAdmin)

# You might not need to register Profile and Address separately if you use Inlines,
# but you can if you want them to appear as separate sections in the admin.
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(SellerProfile) 
