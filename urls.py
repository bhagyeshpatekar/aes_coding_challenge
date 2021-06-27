# from django_db import v
from django.urls import path
from .views import TrnView,InventoryItemView,TransactionDetailView,TransactionDeleteView,LITView
from django.conf.urls import url

app_name = "Transaction"

transaction_urls = [
    path("add_transaction/", TrnView.as_view(), name="add_transaction"),
    path("add_line_item/", LITView.as_view(), name="add_line_item"),
    path(
        "add_inventory_item/",
        InventoryItemView.as_view(),
        name="add_inventory_item",
    ),
    path(
        "delete_transaction/<int:pk>/",
        TransactionDeleteView.as_view(),
        name="delete_transaction",
    ),
    path(
        "transaction_detail/<int:pk>/",
        TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
#    path(r'admin/transaction/transactions_list/$',TrnView.as_view(), name='users_list' ),
]   
