from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.models import User, Transaction
from transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, pk=None):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            user_id = request.data['user']
            payer_id = request.data['payer']
            points = int(request.data['points'])
            # adds or substracts points when creating any valid transaction
            user = User.objects.all().filter(id=user_id)[0]
            user.points += points
            user.save()

            # if points are deducted, deduct from earliest positive payments from the same payer
            if points < 0:
                abs_points = abs(points)
                transactions = Transaction.objects.all().filter(user=user_id).filter(payer=payer_id).filter(points__gt=0).order_by('timestamp')
                for transaction in transactions:
                    if abs_points == 0:
                        break
                    min_deduction = min(transaction.points, abs_points)
                    transaction.points -= min_deduction
                    transaction.save()
                    abs_points -= min_deduction
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
