from django.contrib import admin

from apps.gym.models import Carausel, Category, Contact, CustomUser, Enquery, Equipment\
    , Plan, Member, AccountInfo, Dietmanagement, Trainer, TrainerDepartment

admin.site.register(CustomUser)
admin.site.register(Enquery)
admin.site.register(Equipment)
admin.site.register(Plan)
admin.site.register(Member)
admin.site.register(AccountInfo)
admin.site.register(Dietmanagement)
admin.site.register(Contact)
admin.site.register(TrainerDepartment)
admin.site.register(Category)
admin.site.register(Carausel)

# admin.site.register(Fooditem)
# admin.site.register(UserFooditem)



