from django.contrib import admin
from movie.models import *
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('ch_name', 'region', 'types', 'year','create_date')
    search_fields = ('ch_name', 'other_name', 'down_url', 'video', 'down_name','down_name2')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date')
    date_hierarchy = 'create_date'
    search_fields = ('title',)

class TvAdmin(admin.ModelAdmin):
    list_display = ('ch_name', 'region', 'types', 'year','create_date')
    search_fields = ('ch_name', 'other_name')
    
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('ch_name', 'region', 'types', 'year','create_date')
    search_fields = ('ch_name', 'other_name')
    
class ShowAdmin(admin.ModelAdmin):
    list_display = ('ch_name', 'region', 'types', 'year','create_date')
    search_fields = ('ch_name', 'other_name')

admin.site.register(News, NewsAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Tv, TvAdmin)
admin.site.register(Show, ShowAdmin)

admin.site.register([ 
                     MovieReply, NewsReply,User, User_Message, Index_Slider,
                     Post, PostReply,PostLayerReply, TvReply, Anime,AnimeReply, News_Index_Slider
                     ])


