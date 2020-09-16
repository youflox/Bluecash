from django.conf.urls import url
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenRefreshSlidingView
from rest_framework.authtoken.views import obtain_auth_token

from .views import getAllUsers, DetailsRegisterView, getUser, AddBalanceView,\
    addMoneyTransactionsView,TransferMoneyView,TransferMoneyTransactionsView, AddedMoneyCurrentMonth, TransferredMoneyCurrentMonth


urlpatterns = [
    path('', include('rest_framework.urls')),

    path('accounts/register',DetailsRegisterView.as_view()),
    path('account', getUser),
    path('accounts/profile/', getUser),
    path('accounts/all',getAllUsers ),
    # path('accounts/all', getAllUsers),

    path('accounts/profile/add', AddBalanceView.as_view()),
    path('accounts/profile/transfer', TransferMoneyView.as_view()),

    path('accounts/profile/add/history',addMoneyTransactionsView),
    path('accounts/profile/transfer/history', TransferMoneyTransactionsView),

    path('accounts/profile/add/history/<str:current>', AddedMoneyCurrentMonth),
    path('accounts/profile/transfer/history/<str:current>', TransferredMoneyCurrentMonth),

    path('auth', TokenObtainPairView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view()),
]
