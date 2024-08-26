from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'is_active', 'is_superuser', 'phone', 'custom')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        """
        Create and return a new CustomUser instance, given the validated data.

        Args:
            validated_data (dict): The validated data containing user information.

        Returns:
            CustomUser: The created CustomUser instance.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'].split('@')[0],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Update and return an existing CustomUser instance, given the validated data.

        Args:
            instance (CustomUser): The existing CustomUser instance to update.
            validated_data (dict): The validated data containing updated user information.

        Returns:
            CustomUser: The updated CustomUser instance.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class ResetEmailSerializer(serializers.Serializer):
    """
    Serializer for resetting email.
    """
    email = serializers.EmailField()