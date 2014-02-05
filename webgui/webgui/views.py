# Create your views here.
from django.template import RequestContext
from webgui.models import Diagrams
from django.shortcuts import render_to_response


# def VeloView(request):
#     """Diagram menu"""
#     tabs = Diagrams.objects.all().order_by("-created")
#     return render_to_response("../templates/webgui/VeloView.html", dict(tabs=tabs))


def SensorView(request):
    return render_to_response("../templates/webgui/sensorview.html")


def Overview(request):
    return render_to_response("../templates/webgui/overview.html")


def Trends(request):
    return render_to_response("../templates/webgui/trends.html")


def DetailedTrends(request):
    return render_to_response("../templates/webgui/detailedtrends.html")


def RunView(request):
    return render_to_response("../templates/webgui/runview.html")


def TellView(request):
    return render_to_response("../templates/webgui/tellview.html")


# def SpecialAnalyses(request):
#     return render_to_response("../templates/webgui/specialanalyses.html")


def IVscans(request):
    return render_to_response("../templates/webgui/ivscans.html")


def ITscans(request):
    return render_to_response("../templates/webgui/itscans.html")


def HVscans(request):
    return render_to_response("../templates/webgui/hvscans.html")


def CCEscans(request):
    return render_to_response("../templates/webgui/ccescans.html")


def IPresolution(request):
    return render_to_response("../templates/webgui/ipresolution.html")


def PVresolution(request):
    return render_to_response("../templates/webgui/pvresolution.html")

