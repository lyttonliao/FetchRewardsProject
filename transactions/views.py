from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionDetail(APIView):
    """Retrievee, update, or delete transaction instance"""
    
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk=pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionsList(APIView):
    """List all transactions, or create a new transaction """
    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = request.data['user']
            payer_id = request.data['payer']
            points = request.data['points']
            user = get_user_model().objects.all().filter(id=user_id)[0]
            print(user)
            user.points = user.points + points
            user.save()
            if points < 0:
                i = 0
                transactions = Transaction.objects.all().filter(user_id=user).filter(payer_id=payer_id).order_by('timestamp')
                while points > 0:
                    transaction_points = transactions[i].points
                    if transaction_points > 0:
                        min_deduction = min(points, transaction_points)
                        transactions[i].points = transaction_points - min_deduction
                        transactions[i].save()
                        points, i = points - min_deduction, i + 1

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
