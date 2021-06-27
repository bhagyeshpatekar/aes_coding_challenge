import uuid
from django.db.models.fields import UUIDField
from django.shortcuts import render
from rest_framework.serializers import Serializer
from .models import TransactionModel, Transaction_LID, Inventory_Item
from .serializers import *
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response



class TrnView(generics.CreateAPIView):
    serializer_class = LITDSerializer

    def post(self, request, *args, **kwargs):
        serializer = LITDSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            serializer = TLISerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LITView(generics.CreateAPIView):
    serializer_class = LIDCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = LIDCreateSerializer(data=request.data)
        if serializer.is_valid():
            line_item = serializer.save()
            serializer = LIDCreateSerializer(line_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemView(generics.CreateAPIView):
    serializer_class = TLISerializer 

    def post(self, request, *args, **kwargs):
        serializer = MISerializer(data=request.data)
        if serializer.is_valid():
            inventory_item = serializer.save()
            serializer = LiIIISerializer(inventory_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDeleteView(generics.DestroyAPIView):
    queryset = TransactionModel.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            transaction = TransactionModel.id
        except TransactionModel.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "transaction not found"},
            )
        qs = Transaction_LID.objects.filter(item=transaction)
        if qs.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "cannot delete because line items exists"},
            )
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionDetailView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        #try:
        #    transaction = TransactionModel.id
       # except TransactionModel.DoesNotExist:
         #   return Response(
          #      status=status.HTTP_404_NOT_FOUND,
           #     data={"error": "transaction not found"},
           # )
        line_items = Transaction_LID.objects.filter('id', '')
        inventory_items = []
        for item in line_items:
            inventory_item = Inventory_Item.objects.filter(inventory_item=item)
            inventory_items.append(
                IISerializer(inventory_item, many=True).data
            )
        custom_response = {
            "transaction": TRNDetailSerializer(TransactionModel).data,
            "line_items": LIDCreateSerializer(line_items, many=True).data,
            "inventory_items": inventory_items,
        }
        return Response(custom_response, status=status.HTTP_200_OK)