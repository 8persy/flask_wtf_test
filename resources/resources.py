from flask_marshmallow import Marshmallow
from flask_restful import Resource
from marshmallow import fields as ma_fields, ValidationError
from models.users import Item, db
from flask import request

ma = Marshmallow()


class ItemSchema(ma.Schema):
    id = ma_fields.Integer(dump_only=True)
    name = ma_fields.String(required=True)
    description = ma_fields.String(required=True)


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class ItemResource(Resource):
    def get(self, item_id: int):
        query = Item.query.where(Item.id == item_id)
        item = db.session.execute(query).scalar()

        if item:
            return item_schema.dump(item)
        return {"status": 404}, 404

    def patch(self, item_id: int):
        query = Item.query.where(Item.id == item_id)
        if item := db.session.execute(query).scalar():
            if name := request.json.get("name"):
                item.name = name
            if desc := request.json.get("description"):
                item.description = desc
            db.session.commit()
            return {"status": 200}
        return {"status": 404}, 404

    def delete(self, item_id: int):
        query = Item.query.where(Item.id == item_id)
        if item := db.session.execute(query).scalar():
            db.session.delete(item)
            db.session.commit()
            return {"status": 200}
        return {"status": 404}, 404


class ItemListResource(Resource):
    def get(self):
        items = Item.query.all()
        return items_schema.dump(items)

    def post(self):
        data = request.json

        if not data:
            return {"error": "Request body must be JSON"}, 400

        name = data.get("name")
        description = data.get("description")

        if not name:
            return {"error": "Field 'name' is required and cannot be empty"}, 400

        if not description:
            return {"error": "Field 'description' is required and cannot be empty"}, 400

        try:
            new_item_data = item_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        new_item = Item(name=new_item_data['name'], description=new_item_data['description'])
        db.session.add(new_item)
        db.session.commit()

        return item_schema.dump(new_item), 201