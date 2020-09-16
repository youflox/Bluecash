from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import RegisterSerializer, UserRegisterSerializer, DetailViewSerializer, AddBalanceSerializer, \
    AddMoneyTransactionsModelSerializer, TransferMoneyTransactionsModelSerializer, TransferMoneySerializer

from .models import UserDetailsModel, AddMoneyTransactionsModel, TransferMoneyTransactionsModel

import datetime


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data,status=status.HTTP_201_CREATED)

class DetailsRegisterView(APIView):
    PERMISSION_CLASSES = ('rest_framework.permissions.IsAuthenticated',)
    AUTHENTICATED_CLASSES = ('rest_framework_simplejwt.authentication.JWTAuthentication',)

    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        # print(get_token(request))
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data,status=status.HTTP_201_CREATED)


class AddBalanceView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [JWTAuthentication,]

    serializer_class = AddBalanceSerializer

    def get(self, request):
        user = request.user.id
        queryset = UserDetailsModel.objects.get(user_id=user)
        data = {'Current Balance' : queryset.balance}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user.id, validated_data=user)

        new_balance = UserDetailsModel.objects.get(user_id= request.user.id).balance

        data = {"Credited " : float(user['add']), "Current Balance" : new_balance}
        return Response(data, status=status.HTTP_201_CREATED)


class TransferMoneyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication, ]

    serializer_class = TransferMoneySerializer

    def get(self, request):
        user = request.user.id
        queryset = UserDetailsModel.objects.get(user_id=user)
        # serializer_class = DetailViewSerializer(queryset)

        data = {'Current Balance' : float(queryset.balance)}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user.id, validated_data=data)

        new_balance = UserDetailsModel.objects.get(user_id= request.user.id).balance

        data = {"Current Balance" : new_balance}
        return Response(data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAllUsers(request):
    queryset = UserDetailsModel.objects.all()
    serializer_class  = DetailViewSerializer(queryset, many=True)
    return Response(serializer_class.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def addMoneyTransactionsView(request):

    user = request.user.id
    queryset = AddMoneyTransactionsModel.objects.all().filter(user_id=user)
    serializer_class = AddMoneyTransactionsModelSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def TransferMoneyTransactionsView(request):
    user = request.user.id
    queryset = TransferMoneyTransactionsModel.objects.all().filter(user_id=user)
    serializer_class = TransferMoneyTransactionsModelSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def AddedMoneyCurrentMonth(request, current):

    total = 0

    start_of_month = datetime.date.today().replace(day=1)
    user = request.user.id
    added_this_month = AddMoneyTransactionsModel.objects.all().filter(user_id=user).filter(time__gte= start_of_month)
    serializer_class = AddMoneyTransactionsModelSerializer(added_this_month, many=True)

    for data in serializer_class.data:
        total += float(data['credited'])

    return Response({"Added this month " : total})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TransferredMoneyCurrentMonth(request, current):

    user = request.user.id
    start_of_month = datetime.date.today().replace(day=1)

    transfers_this_month = TransferMoneyTransactionsModel.objects.filter(user_id=user).filter(time__gte=start_of_month)
    serializer_class = TransferMoneyTransactionsModelSerializer(transfers_this_month, many=True)

    total = 0
    for data in serializer_class.data:
        total += float(data['debited'])

    return Response({"Transferred this month " : total})



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getUser(request):

    start_of_month = datetime.date.today().replace(day=1)
    addedTotal = 0
    transferredTotal = 0
    user = request.user

    user_detail = UserDetailsModel.objects.get(user_id=user)
    user_detail_serializer = DetailViewSerializer(user_detail)

    transfers_this_month = TransferMoneyTransactionsModel.objects.filter(user_id=user).filter(time__gte=start_of_month)
    transfers_this_month_serializer = TransferMoneyTransactionsModelSerializer(transfers_this_month, many=True)

    added_this_month = TransferMoneyTransactionsModel.objects.all().filter(user_id=user).filter(time__gte=start_of_month)
    added_this_month_serializer = TransferMoneyTransactionsModelSerializer(added_this_month, many=True)

    for addedData in added_this_month_serializer.data:
        addedTotal += float(addedData['debited'])

    for transferData in transfers_this_month_serializer.data:
        transferredTotal += float(transferData['debited'])

    data = {
        'Wallet Id' : user.id,
        'User Name' : str(user.username).title(),
        'Total Sum of money added to wallet for the current month' : addedTotal,
        'Total Sum of money paid to to other users for the current month': addedTotal,
        'Current Wallet Balance' : float(user_detail_serializer.data['balance'])

    }


    return Response(data)


