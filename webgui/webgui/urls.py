__author__ = 'Pavlo'

from webgui import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.Overview, name='Overview'),
    url(r'^sensorview/$', views.SensorView, name='SensorView' ),
    url(r'^runview/$', views.RunView, name='RunView'),
    url(r'^trends/$', views.Trends, name='Trends'),
    url(r'^detailedtrends/$', views.DetailedTrends, name='DetailedTrends'),
    url(r'^tellview/$', views.TellView, name='TellView'),
    # url(r'^specialanalyses/$', views.SpecialAnalyses, name='SpecialAnalyses'),
    url(r'^ivscans/$', views.IVscans, name='IVscans'),
    url(r'^itscans/$', views.ITscans, name='ITscans'),
    url(r'^hvscans/$', views.HVscans, name='HVscans'),
    url(r'^ccescans/$', views.CCEscans, name='CCEscans'),
    url(r'^ipresolution/$', views.IPresolution, name='IPresolution'),
    url(r'^pvresolution/$', views.PVresolution, name='PVresolution'),
    # url(r'^$', views.VeloView, name='VeloView'),
)