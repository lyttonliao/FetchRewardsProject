import collections
from rest_framework import viewsets
from core.models import User, Transaction
from users.serializers import UserSerializer
from transactions.serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """Viewset to Create, List, Retrieve, Delete User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def retrieve(self, request, pk=None):
        user_points_per_company = collections.Counter()
        transactions = Transaction.objects.all().filter(user=pk).filter(points__gte=0).order_by('timestamp')
        for transaction in transactions:
            user_points_per_company[transaction.payer.company] += transaction.points
        return Response(user_points_per_company)


    def partial_update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        instance = self.queryset.filter(id=user_id)[0]
        points = int(request.data['points'])
        serializer = self.serializer_class(instance, data={'points': instance.points - points}, partial=True)

        # calls to spend player points must be positive
        if serializer.is_valid() and points > 0:
            transactions = Transaction.objects.all().filter(user=user_id).filter(points__gt=0).order_by('timestamp')
            new_transactions = []
            # deduct points from the user's earliest positive transactions until all points are spent
            for transaction in transactions:
                if points == 0:
                    break
                min_deduction = min(transaction.points, points)
                transaction.points -= min_deduction
                transaction.save()
                transaction_data = {
                    'user': transaction.user.id, 
                    'payer': transaction.payer.id, 
                    'points': -min_deduction, 
                }
                response_data = {
                    'payer': transaction.payer.company,
                    'points': -min_deduction
                }
                transaction_serializer = TransactionSerializer(data=transaction_data)
                # create and serialize new transactions, saved if they're valid
                if transaction_serializer.is_valid():
                    new_transactions.append(response_data)
                    transaction_serializer.save()
                else:
                    Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                points -= min_deduction
            serializer.save()
            return Response(new_transactions)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        