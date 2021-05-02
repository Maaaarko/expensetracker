from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import GoogleAuthSerializer

class GoogleAuthView(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        
        data = (serializer.validated_data["auth_token"])
        return Response(data, status=status.HTTP_200_OK)