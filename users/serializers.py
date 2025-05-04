from rest_framework import serializers
from .models import CustomUser, ClientProfile

class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ClientProfile
        fields = ['id', 'user', 'nom', 'prenom', 'adresse', 'solde_de_credit']

class CustomUserSerializer(serializers.ModelSerializer):
    client_profile = ClientProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'role', 'location',
            'first_name', 'last_name', 'is_staff', 'is_active',
            'client_profile', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance