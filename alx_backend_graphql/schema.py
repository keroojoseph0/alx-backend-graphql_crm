import graphene
from crm.schema import CRMQuery, Mutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(Mutation, graphene.ObjectType):
    pass
    
schema = graphene.Schema(query=Query, mutation=Mutation)