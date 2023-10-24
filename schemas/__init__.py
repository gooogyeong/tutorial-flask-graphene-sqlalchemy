from graphene import relay, ObjectType, Schema, Mutation, String, Field, Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from db import session, User as UserDBModel, Post as PostDBModel


class UserSchema(SQLAlchemyObjectType):  # instead of ObjectType coming from graphene
    class Meta:
        model = UserDBModel
        interfaces = (relay.Node,)


class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = PostDBModel
        interfaces = (relay.Node,)


class Query(ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserSchema.connection)
    all_posts = SQLAlchemyConnectionField(PostSchema.connection)


class UserMutation(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)

    user = Field(lambda: UserSchema)

    def mutate(self, info, username, email):
        user = UserDBModel(username=username, email=email)
        session.add(user)
        session.commit()
        return UserMutation(user=user)  # so that it returns user that has been created


class PostMutation(Mutation):
    class Arguments:
        title = String(required=True)
        content = String(required=True)
        user_id = Int(required=True)

    post = Field(lambda: PostSchema)

    def mutate(self, info, title, content, user_id):
        author = session.query(UserDBModel).filter_by(id=user_id).first()

        post = PostDBModel(title=title, content=content, author=author)
        session.add(post)
        session.commit()
        return PostMutation(post=post)


class Mutation(ObjectType):
    create_user = UserMutation.Field()
    create_post = PostMutation.Field()


schema = Schema(query=Query, mutation=Mutation)
