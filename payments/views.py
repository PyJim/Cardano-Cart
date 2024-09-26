from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from pycardano import Address, Network, PaymentVerificationKey, StakeVerificationKey

class GeneratePaymentAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the authenticated user
        user = request.user
        
        # Retrieve the wallet_id from the user model (this should be the user's public key)
        wallet_id = '593a9a909106e2db66ca9fc35cefcb77ba9adb1b5fce35ff01efa4a17c4e2366e9a3201317d1f6b951c6003875e7ae9aec5b144834ad12e1cfc77589b085fe98' #user.wallet_id
        
        if not wallet_id:
            return Response({"error": "User does not have a wallet ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Generate a payment address using the user's wallet_id (which should be a public key)
            # Use testnet
            network = Network.TESTNET

            # Replace this with your actual public payment key (in hex format)
            payment_key_hex = wallet_id  # Example: "f4b78d2d6a0d6..."

            # Create a PaymentVerificationKey object from the public key hex
            pvk = PaymentVerificationKey.from_bytes(bytes.payment_key_hex)

            # Since you might not have a stake key, we'll use a null stake key
            null_stake_key = StakeVerificationKey.NULL

            # Derive the address using the payment verification key and a null stake verification key
            address = Address(pvk.hash(), null_stake_key.hash(), network)

            # Return the generated address
            return Response({
                "message": "Payment address generated successfully",
                "payment_address": str(address)
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
