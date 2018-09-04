from django.contrib import admin

from .models import District, DistrictType, MembershipType, Group, GroupType, SavedSearch

class DistrictAdmin(admin.ModelAdmin):
    list_display = ( "name", "districttype", "van_id")
    ordering = ("districttype__order", "name",)

admin.site.register(District, DistrictAdmin)

class DistrictTypeAdmin(admin.ModelAdmin):
    list_display = ( "name", )
    ordering = ("order", "name")

admin.site.register(DistrictType, DistrictTypeAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ( "name", "grouptype", "protect")
    ordering = ("grouptype__order", "name",)

admin.site.register(Group, GroupAdmin)

class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ( "name", )
    ordering = ("order", "name")

admin.site.register(GroupType, GroupTypeAdmin)

class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ( "name", "counts_quorum")
    ordering = ("order", "name")

admin.site.register(MembershipType, MembershipTypeAdmin)

class SavedSearchAdmin(admin.ModelAdmin):
    pass

admin.site.register(SavedSearch, SavedSearchAdmin)
