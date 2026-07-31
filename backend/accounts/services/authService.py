from .clerk_verification import ClerkVerificationService
from ipware import get_client_ip
# from .google import GoogleService
# from .facebook import FacebookService


class AuthService:
    @staticmethod
    def login(request, provider, device):
        """
        Flow
        1. Determine the authentication provider.
        2. Verify the provider token and email.
        3. Check if the user exists; create if not.
        4. Create JWT tokens.
        5. Store the refresh token and device data in the user session.
        6. Create a login history record.
        7. Return the JWT tokens.
        """

        inware_ip = get_client_ip(request)

        if inware_ip:
            ip_address, _ = get_client_ip(request)

        print(f"IP Address: {ip_address}")

        if provider == "clerk":
            provider_user = ClerkVerificationService.verify(request)

        # elif provider == "google":
        #     provider_user = GoogleService.verify(request)

        # elif provider == "facebook":
        #     provider_user = FacebookService.verify(request)

        else:
            raise ValueError("Unsupported authentication provider.")

        # TODO:
        # user = UserService.get_or_create(provider_user)
        # tokens = JWTService.create_tokens(user)
        # UserSessionService.create(user, tokens["refresh"], device)
        # LoginHistoryService.create(user, device)

        return provider_user