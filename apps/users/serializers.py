from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'profile_image')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'first_name', 
                  'last_name', 'date_joined', 'profile_image')       

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        user = User.objects.create(
            username=validated_data['username'],
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    class Meta:
        model = User 
        fields = ('id','username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

