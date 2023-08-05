from books.models import Review
from rest_framework.response import Response
from .serializers import ReviewSerializer
from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets


class ReviewViewSet(viewsets.ViewSet):
    serializer_class=ReviewSerializer
    lookup_url_kwarg = 'review_id'

    def list(self,request):
        serializer=self.serializer_class(Review.objects.all().order_by('-created_at'),many=True)
        return Response(data=serializer.data)

    def retrieve(self,request,review_id):
        review=Review.objects.get(id=review_id)
        serializer=self.serializer_class(review)
        return Response(serializer.data)

    def create(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

    def partial_update(self):
        pass


class ReviewModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().order_by('-created_at')
    lookup_url_kwarg = 'review_id'


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_url_kwarg = 'review_id'


class ReviewListAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().order_by('-created_at')


# class ReviewDetailAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self,request,review_id):
#         review=Review.objects.get(id=review_id)
#         serializer=ReviewSerializer(instance=review)
#         return Response(serializer.data)
#
#     def put(self,request,review_id):
#         review=Review.objects.get(id=review_id)
#         serializer=ReviewSerializer(instance=review,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data,status=status.HTTP_200_OK)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self,request,review_id):
#         review = Review.objects.get(id=review_id)
#         serializer = ReviewSerializer(instance=review, data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,review_id):
#         review=Review.objects.get(id=review_id)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ReviewListAPIView(APIView):
#
#     def get(self,request):
#         reviews=Review.objects.all().order_by('-created_at')
#
#         paginator=PageNumberPagination()
#         page_obj=paginator.paginate_queryset(reviews,request)
#
#         serializer=ReviewSerializer(page_obj,many=True)
#         return paginator.get_paginated_response(serializer.data)
#
#     def post(self,request):
#         serializer=ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data,status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUES
