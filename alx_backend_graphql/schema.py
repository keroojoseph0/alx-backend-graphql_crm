import graphene

class CRMQuery(graphene.ObjectType):
    customer_count = graphene.Int()

    def resolve_customer_count(root, info):
        return 42

class Query(CRMQuery, graphene.ObjectType):
    hello = graphene.String()
    
    def resolve_hello(root, info):
        return "Hello, GraphQL!"
    
schema = graphene.Schema(query=Query)