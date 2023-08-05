from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Book, Review
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('id','first_name','last_name','username','email')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=('id','title','isbn','description')


class ReviewSerializer(serializers.ModelSerializer):
    book=BookSerializer(read_only=True)
    user=UserSerializer(read_only=True)
    book_id=serializers.IntegerField(write_only=True,required=False)
    user_id=serializers.IntegerField(write_only=True,required=False)

    class Meta:
        model = Review
        fields=('id','stars_given','comment','user','book','book_id','user_id')

    def update(self, instance, validated_data):
        if not validated_data.get('book_id'):
            validated_data['book_id'] = instance.book_id
        if not validated_data.get('user_id'):
            validated_data['user_id'] = instance.user_id
        return super().update(instance,validated_data)

    def create(self, validated_data):
        if not validated_data.get('book_id'):
            raise ValidationError({
                "success":False,
                "message":"book_id is a required field."
            })
        if not validated_data.get('user_id'):
            raise ValidationError({
                "success": False,
                "message": "user_id is a required field."
            })
        return super().create(validated_data)

