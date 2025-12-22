from django.db import IntegrityError
from django.forms import ValidationError
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Customer, Product, Order

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone')

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock = 0):
        new_product = Product.objects.create(
            name = name,
            price = price,
            stock = stock
        )
        new_product.save()
        return CreateProduct(product = new_product)

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        email = graphene.String(required = True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)

    def mutate(self, info, name, email, phone = None):
        customer = Customer.objects.create(
            name = name,
            email = email,
            phone = phone
        )
        customer.save()
        return CreateCustomer(customer=customer)
    
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):

        if not product_ids:
            raise GraphQLError("At least one product must be selected.")

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID.")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise GraphQLError("Invalid product ID.")

        order = Order.objects.create(
            customer_id=customer,
            order_date=order_date
        )

        order.product_ids.set(products)

        return CreateOrder(order=order)


class CustomerInpute(graphene.InputObjectType):
    name = graphene.String(required = True)
    email = graphene.String(required = True)
    phone = graphene.String()

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInpute, required = True)

    created_customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(root, info, customers):
        created_customers = []
        errors = []

        # Wrap in atomic block to control transactions per record
        for idx, customer_data in enumerate(customers):
            try:
                # Create a Customer instance but don't commit yet
                customer = Customer(**customer_data)
                customer.full_clean()  # runs model validation
                customer.save()
                created_customers.append(customer)
            except ValidationError as ve:
                errors.append(f"Customer {idx + 1}: {ve.message_dict}")
            except IntegrityError as ie:
                errors.append(f"Customer {idx + 1}: {str(ie)}")
            except Exception as e:
                errors.append(f"Customer {idx + 1}: {str(e)}")

        return BulkCreateCustomers(created_customers=created_customers, errors=errors)


class CRMQuery(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    customer = graphene.Field(CustomerType, id=graphene.Int())

    def resolve_all_customer(root, info):
        return Customer.objects.all()

    def resolve_customer(root, info, id):
        customer = Customer.objects.get(pk=id)
        return customer

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()