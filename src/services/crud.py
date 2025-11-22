from sqlalchemy.orm import Session
from typing import TypeVar, Generic
from sqlalchemy import select, insert, delete

M = TypeVar('M')

class CrudService(Generic[M]):
    def __init__(self, session: Session, model: M):
        self.session = session  
        self.model = model

    def create(self, payload) :
        model_instance = self.model(**payload)
        self.session.add(model_instance)
        self.session.commit()
        self.session.refresh(model_instance)
        return model_instance

    def create_bulk(self, payloads: list):
        data = [payload.model_dump() for payload in payloads]
        print(data)
        obj_ids = self.session.scalars(insert(self.model).returning(self.model.id, sort_by_parameter_order=True), data).all()
        self.session.commit()
        objs = (self.session.query(self.model)
            .filter(self.model.id.in_(obj_ids))
            .all())        
        return objs
        
    def get_all(self):
        stmt = select(self.model)
        objs = self.session.scalars(stmt).all()
        return objs

    def get(self, obj_id):
        obj = self.session.get(self.model, obj_id)
        return obj

    def update(self, obj_id, obj_in):
        obj = self.session.get(self.model, obj_id)
        for key, value in obj_in.items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj_id):
        obj = self.session.get(self.model, obj_id)
        self.session.delete(obj)
        self.session.commit()
        return obj

    def delete_all(self):
        objs = self.session.scalars(select(self.model)).all()
        self.session.execute(delete(self.model))
        self.session.commit()
        print(objs)
        return objs
