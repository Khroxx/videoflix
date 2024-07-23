from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'phone', 'custom')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'].split('@')[0],
            # password=validated_data['password'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class ResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()