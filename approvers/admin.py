from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_display = ('username', 'email', 'is_staff', 'get_role')
    list_select_related = ('profile', )

    def get_role(self, instance):
        return instance.profile.role
    get_role.short_description = 'Role'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

#---------

# class Profile(models.Model):
#     STUDENT = 1
#     TEACHER = 2
#     SUPERVISOR = 3
#     ROLE_CHOICES = (
#         (STUDENT, 'Student'),
#         (TEACHER, 'Teacher'),
#         (SUPERVISOR, 'Supervisor'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     location = models.CharField(max_length=30, blank=True)
#     birthdate = models.DateField(null=True, blank=True)
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

#     def __str__(self):  # __unicode__ for Python 2
#         return self.user.username

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

