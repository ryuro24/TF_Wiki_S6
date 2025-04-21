from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print("⚙️ pre_social_login triggered")

        email = sociallogin.user.email
        print(f"📨 Email received from Google: {email}")

        try:
            user = get_user_model().objects.get(email=email)
            print(f"✅ Found existing user: {user}")
        except get_user_model().DoesNotExist:
            user = None
            print("❌ No user found with this email")

        if user:
            print("🔗 Associating social account with existing user")
            sociallogin.user = user
        else:
            print("🆕 Creating new user for Google login")
            user = get_user_model().objects.create_user(
                email=email,
                username=f"user_{get_random_string(8)}"
            )
            print(f"👤 New user created: {user}")
            sociallogin.user = user