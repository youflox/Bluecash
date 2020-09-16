from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import UserDetailsModel, TransferMoneyTransactionsModel, AddMoneyTransactionsModel


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only = True, required=True)

    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','password')
        read_only_fields = ('id',)


class UserRegisterSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = UserDetailsModel
        fields = ('phone','user')

    # def validate(self, attrs):
    #     pass
    def create(self, validated_data):
        # password = validated_data['user']['password']
        if validated_data.get('user'):
            validated_data['user']['password'] = make_password(validated_data['user']['password'])

        user_data = validated_data.pop('user')
        user = RegisterSerializer.create(RegisterSerializer(), validated_data=user_data)
        data, created = UserDetailsModel.objects.update_or_create(user=user, phone=validated_data.pop('phone'))

        return data


class DetailViewSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)
    class Meta:
        model = UserDetailsModel
        fields = ('user','phone','balance')


class AddBalanceSerializer(serializers.ModelSerializer):
    add = serializers.CharField(required=True,write_only=True)

    class Meta:
        model = UserDetailsModel
        fields = ('add','balance')
        read_only_fields = ('balance',)

    def save(self, instance, validated_data):
        # data, created = UserDetailsModel.objects.update_or_create(user_id=instance, balance=validated_data['add'])

        user = UserDetailsModel.objects.get(user_id = instance)
        user.balance = float(user.balance)+ float(validated_data['add'])
        user.save()
        saveTransaction = AddMoneyTransactionsModel.objects.create(credited=(validated_data['add']),
                                                 total = user.balance, user=User.objects.get(id=instance))
        saveTransaction.save()



class TransferMoneySerializer(serializers.ModelSerializer):
    to_phone = serializers.CharField(source='User.phone')
    amount = serializers.DecimalField(required=True, allow_null=False, decimal_places=2, max_digits=10 )

    class Meta:
        model = UserDetailsModel
        fields = ('to_phone','amount')
        read_only_fields = ('balance',)


    def save(self, instance, validated_data):
        from_details = UserDetailsModel.objects.get(user_id=instance)
        phone = validated_data['to_phone']
        amount = validated_data['amount']
        to = UserDetailsModel.objects.get(phone=phone)

        if float(from_details.balance) >= float(amount):
            if to:
                from_details.balance = float(from_details.balance) - float(amount)
                to.balance = float(to.balance) + float(amount)

                to.save()
                from_details.save()

                # print(User.objects.get(id=instance), amount, from_details.balance)

                saveTransaction = TransferMoneyTransactionsModel.objects.create(to=str(to.user),
                                                                           debited = amount,
                                                                           balance=from_details.balance,
                                                                           user_id=instance)
                saveTransaction.save()


class AddMoneyTransactionsModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = AddMoneyTransactionsModel
            fields = ('credited','time','total')


class TransferMoneyTransactionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferMoneyTransactionsModel
        fields = ('to', 'debited','balance', 'time')
