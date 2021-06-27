from rest_framework import serializers
from .models import TransactionModel,Transaction_LID,Inventory_Item

class LIDCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_LID
        fields = "__all__"

    def create(self, validated_data):
        return Transaction_LID.objects.create(**validated_data)


class TRNDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = "__all__"


class LIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_LID
        fields = "__all__"


class Inventory_ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_Item
        fields = "__all__"


class LITDSerializer(serializers.ModelSerializer):
    line_items = LIDSerializer(many=True, write_only=True)

    class Meta:
        model = TransactionModel
        fields = "__all__"

   


class IISerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory_Item
        fields = "__all__"

    def create(self, validated_data):
        return Inventory_Item.objects.create(**validated_data)


class TLISerializer(serializers.ModelSerializer):
    line_items = serializers.SerializerMethodField()

    class Meta:
        model = TransactionModel
        fields = "__all__"

  #  def get_line_items(self, object):
  #      line_items = Transaction_LID.objects.filter(item=object)
   #     return LIDSerializer(line_items, many=True, null=True).data


class MISerializer(serializers.ModelSerializer):
    inventory_items = IISerializer(many=True, write_only=True)

    class Meta:
        model = Transaction_LID
        fields = "__all__"

    def create(self, validated_data):
        inventory_items = validated_data.pop("inventory_items", [])
        inventory_item = Transaction_LID.objects.create(**validated_data)
        for item in inventory_items:
            item["inventory_item"] = inventory_item
            Inventory_Item.objects.create(**item)
        return inventory_item


class LiIIISerializer(serializers.ModelSerializer):
    inventory_items = serializers.SerializerMethodField()

    class Meta:
        model = Transaction_LID
        fields = "__all__"

    def get_inventory_items(self, object):
        inventory_items = Inventory_Item.objects.filter(inventory_item=object)
        return IISerializer(inventory_items, many=True).data