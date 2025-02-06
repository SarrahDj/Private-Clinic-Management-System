from rest_framework import serializers
from ..models import Bill, ServiceCharge, PaymentTransaction, Invoice



class InvoiceSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    patient = serializers.CharField(source='bill.patient')
    bill_date = serializers.DateTimeField(source='bill.bill_date')
    due_date = serializers.DateTimeField(source='bill.due_date')
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='bill.total_amount')
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='bill.paid_amount')
    status = serializers.CharField(source='bill.status')
    notes = serializers.CharField(source='bill.notes', allow_null=True)
    payment_method = serializers.SerializerMethodField()


    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'bill', 'created_at',
            'patient', 'bill_date', 'due_date', 'total_amount',
            'paid_amount', 'status', 'notes', 'items','payment_method'
        ]
        read_only_fields = ['invoice_number', 'created_at']

    def get_items(self, obj):
            service_charges = obj.bill.servicecharge_set.all()
            return [{
                'description': charge.service,
                'quantity': float(charge.quantity),
                'base_price': float(charge.base_cost),
                'amount': float(charge.total_cost)
            } for charge in service_charges]

    def get_payment_method(self, obj):
        # Get the most recent payment transaction
        payment = obj.bill.paymenttransaction_set.order_by('-transaction_date').first()
        if payment and payment.payment_method:
            # Convert snake_case to readable format
            return payment.payment_method.replace('_', ' ').title()
        return None


class ServiceChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCharge
        fields = ['service', 'description', 'base_cost', 'quantity', 'total_cost']


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['amount', 'payment_method', 'transaction_date', 'status']


class CreateBillSerializer(serializers.Serializer):
    # Bill fields
    patient = serializers.CharField()
    bill_date = serializers.DateTimeField()
    due_date = serializers.DateTimeField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    status = serializers.CharField()
    notes = serializers.CharField(required=False, allow_null=True)

    # Related fields
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    payment_method = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        payment_method = validated_data.pop('payment_method', None)

        # Create the bill
        bill = Bill.objects.create(**validated_data)

        # Create service charges
        for item in items_data:
            ServiceCharge.objects.create(
                bill=bill,
                service=item['description'],
                description=item['description'],
                base_cost=item['unit_price'],
                quantity=item['quantity'],
                total_cost=item['amount']
            )

        # Create payment transaction if payment method exists
        if payment_method:
            PaymentTransaction.objects.create(
                bill=bill,
                amount=validated_data.get('paid_amount', 0),
                payment_method=payment_method.lower().replace(' ', '_'),
                transaction_date=validated_data['bill_date'],
                status='success' if validated_data['status'].lower() == 'paid' else 'pending'
            )

        # Create invoice
        Invoice.objects.create(bill=bill)

        return bill

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        payment_method = validated_data.pop('payment_method', None)

        # Update bill fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update service charges
        instance.servicecharge_set.all().delete()
        for item in items_data:
            ServiceCharge.objects.create(
                bill=instance,
                service=item['description'],
                description=item['description'],
                base_cost=item['unit_price'],
                quantity=item['quantity'],
                total_cost=item['amount']
            )

        # Update payment transaction if payment method exists
        if payment_method:
            PaymentTransaction.objects.filter(bill=instance).delete()
            PaymentTransaction.objects.create(
                bill=instance,
                amount=validated_data.get('paid_amount', 0),
                payment_method=payment_method.lower().replace(' ', '_'),
                transaction_date=validated_data['bill_date'],
                status='success' if validated_data['status'].lower() == 'paid' else 'pending'
            )

        return instance
