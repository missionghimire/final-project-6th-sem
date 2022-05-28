from django.contrib import admin

from apps.gym.models import Contact, CustomUser, Enquery, Equipment, Plan, Member, AccountInfo, Dietmanagement

admin.site.register(CustomUser)
admin.site.register(Enquery)
admin.site.register(Equipment)
admin.site.register(Plan)
admin.site.register(Member)
admin.site.register(AccountInfo)
admin.site.register(Dietmanagement)
admin.site.register(Contact)
