from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from covidPortalApp.views import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

admin.autodiscover()

urlpatterns = [
    url(r'^explorer/', include('explorer.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^covidPortalApp/submitUploadFile/', submitUploadFile, name = 'submitUploadFile'),
    url(r'^covidPortalApp/signupUser/', signupUser, name = 'signupUser'),
    url(r'^covidPortalApp/checkUser/', checkUser, name = 'checkUser'),
    url(r'^covidPortalApp/checkEmail/', checkEmail, name = 'checkEmail'),
    url(r'^covidPortalApp/checkLogin/', checkLogin, name = 'checkLogin'),
    url(r'^covidPortalApp/resetPassword/', resetPassword, name = 'resetPassword'),
    url(r'^covidPortalApp/emailPasswordLink/', emailPasswordLink, name = 'emailPasswordLink'),
    url(r'^covidPortalApp/logoutUser/', logoutUser, name = 'logoutUser'),
    url(r'^covidPortalApp/listUploadedFiles/', listUploadedFiles, name = 'listUploadedFiles'),
    url(r'^covidPortalApp/getDatafile/', getDatafile, name = 'getDatafile'),
    url(r'^covidPortalApp/saveComment/', saveComment, name = 'saveComment'),
    url(r'^covidPortalApp/fetchAllComments/', fetchAllComments, name = 'fetchAllComments'),
    url(r'^covidPortalApp/fetchCommentsByLocation/', fetchCommentsByLocation, name = 'fetchCommentsByLocation'),
    url(r'^covidPortalApp/deleteDatafile/', deleteDatafile, name = 'deleteDatafile'),
    url(r'^covidPortalApp/submitAnalysis/', submitAnalysis, name = 'submitAnalysis'),

    url(r'^covidPortalApp/getMutationData/', getMutationData, name = 'getMutationData'),
    url(r'^covidPortalApp/listSequences/', listSequences, name = 'listSequences'),
    url(r'^covidPortalApp/showAlignment/', showAlignment, name = 'showAlignment'),

    url(r'^covidPortalApp/updateDatafileName/', updateDatafileName, name = 'updateDatafileName'),
    url(r'^covidPortalApp/searchUploadedFolders/', searchUploadedFolders, name = 'searchUploadedFolders'),
    url(r'^covidPortalApp/getUserProfile/', getUserProfile, name = 'getUserProfile'),
    url(r'^covidPortalApp/updateUser/', updateUser, name = 'updateUser'),
    url(r'^covidPortalApp/getRunningJobs/', getRunningJobs, name = 'getRunningJobs'),
    url(r'^covidPortalApp/terminateJob/', terminateJob, name = 'terminateJob'),
    url(r'^covidPortalApp/api-token-auth/', obtain_jwt_token),
    url(r'^covidPortalApp/api-token-refresh/', refresh_jwt_token),

    url('accounts/', include('django.contrib.auth.urls')), # new
    url(r'^admin/', admin.site.urls),

]

urlpatterns += staticfiles_urlpatterns()

#print str(urlpatterns)
