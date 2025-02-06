from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from ..models import Bill, ServiceCharge, PaymentTransaction, Invoice
from ..serializers import (
    CreateBillSerializer, InvoiceSerializer
)


@api_view(['GET'])
def billing_list(request):
    """Get all bills with filtering"""
    queryset = Invoice.objects.select_related('bill').all()

    # Apply search
    search_query = request.query_params.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(invoice_number__icontains=search_query) |
            Q(bill__patient__icontains=search_query)
        )

    # Apply filters
    status_filter = request.query_params.get('payment_status')
    if status_filter:
        queryset = queryset.filter(bill__status=status_filter.lower())

    payment_method = request.query_params.get('payment_method')
    if payment_method:
        queryset = queryset.filter(
            bill__paymenttransaction__payment_method=payment_method.lower().replace(' ', '_')
        ).distinct()

    billing_date = request.query_params.get('billing_date')
    if billing_date:
        queryset = queryset.filter(bill__bill_date__date=billing_date)

    due_date = request.query_params.get('due_date')
    if due_date:
        queryset = queryset.filter(bill__due_date__date=due_date)

    serializer = InvoiceSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def billing_detail(request, pk):
    """Get single bill details"""
    try:
        invoice = Invoice.objects.select_related('bill').get(pk=pk)
    except Invoice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data)


@api_view(['POST'])
@transaction.atomic
def billing_create(request):
    """Create new bill with related records"""
    try:
        serializer = CreateBillSerializer(data=request.data)
        if serializer.is_valid():
            bill = serializer.save()
            invoice = Invoice.objects.get(bill=bill)
            return Response(
                InvoiceSerializer(invoice).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@transaction.atomic
def billing_update(request, pk):
    """Update existing bill and related records"""
    try:
        invoice = Invoice.objects.select_related('bill').get(pk=pk)
    except Invoice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = CreateBillSerializer(invoice.bill, data=request.data)
        if serializer.is_valid():
            bill = serializer.save()
            return Response(InvoiceSerializer(invoice).data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])
@transaction.atomic
def billing_delete(request, pk):
    """Delete bill and related records"""
    try:
        invoice = Invoice.objects.get(pk=pk)
        invoice.delete()  # This will cascade delete related records
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Invoice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def print_invoice(request, pk):
    """Generate printable invoice"""
    try:
        invoice = Invoice.objects.get(pk=pk)
        return Response({'status': 'Invoice ready for printing'})
    except Invoice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)