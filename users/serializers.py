from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Referral

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")
        return value

    def create(self, validated_data):
        referral_code_input = validated_data.pop('referral_code', None)
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        
        if referral_code_input:
            try:
                referrer = User.objects.get(referral_code=referral_code_input)
                if referrer == user:
                    raise serializers.ValidationError("You cannot refer yourself.")
                user.referred_by = referrer
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code.")
        user.save()

        
        if user.referred_by:
            from .models import Referral  
            Referral.objects.create(referrer=user.referred_by, referred_user=user, status='successful')
        return user

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")
        user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()
        if user and user.check_password(password):
            data["user"] = user
            return data
        raise serializers.ValidationError("Invalid credentials.")

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ReferralSerializer(serializers.ModelSerializer):
    referred_username = serializers.CharField(source='referred_user.username', read_only=True)
    date_referred = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Referral
        fields = ['id', 'referred_username', 'date_referred', 'status']

class ReferralStatsSerializer(serializers.Serializer):
    total_referrals = serializers.IntegerField()
    successful_referrals = serializers.IntegerField()
