from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover();
urlpatterns = patterns('',
#url(r'^admin/',include(admin.site.urls)),
url(r'^$', 'search.views.home',name='home'),
url(r'^admin/', admin.site.urls),
url(r'^home/$', 'search.views.home',name='home'),
url(r'^login/$', 'search.views.login',name='login'),
url(r'^register/$', 'search.views.regist',name='registration'),
url(r'^regist_success/$', 'search.views.regist_success',name='regist_success'),
url(r'^profile/$', 'search.views.profile',name='profile'),
url(r'^myorder/$', 'search.views.myorder',name='myorder'),
url(r'^remove_order/$', 'search.views.remove_order',name='remove_order'),
url(r'^logout/$', 'search.views.logout',name='logout'),
url(r'^searchresult/$', 'search.views.SearchBook',name='SearchBook'),
url(r'^shoppingcart/$', 'search.views.view_cart',name='ShowCart'),

url(r'^shoppingcart/show/$', 'search.views.show', name='carton-tests-show'),
url(r'^shoppingcart/add/$', 'search.views.add', name='carton-tests-add'),
url(r'^shoppingcart/clean/$', 'search.views.clean_cart', name='clean_cart'),
url(r'^shoppingcart/submitorder/$', 'search.views.SubmitOrder', name='SubmitOrder'),
url(r'^shoppingcart/checkout/$', 'search.views.CheckOut', name='CheckOut'),
url(r'^shoppingcart/remove_item/$', 'search.views.remove_item', name='remove_item'),
url(r'^shoppingcart/change_item_quantity/$', 'search.views.change_item_quantity', name='change_item_quantity'),

)
