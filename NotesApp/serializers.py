from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator




class NoteSerializer(serializers.ModelSerializer):
    is_shared = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'user', 'created', 'updated', 'is_shared']
        read_only_fields = ('user', 'created', 'updated')

    def get_is_shared(self, obj):
        request = self.context['request']
        return obj.shared_users.filter(pk=request.user.pk).exists()


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'bio')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_internal_value(self, data):
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, bytes):
                cleaned_data[key] = value.decode('utf-8', errors='replace')
            else:
                cleaned_data[key] = value
        return super().to_internal_value(cleaned_data)