from store_Monitoring import db


def commit_changes():
    db.session.commit()


def get_all(model):
    data = model.query.all()
    return data


def get_filter_by(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    return instance


def get_filter_all(model, **kwargs):
    instance = model.query.filter_by(**kwargs).all()
    return instance


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def edit_instance(model, id, **kwargs):
    instance = model.query.filter_by(id=id).first()
    for attr, new_val in kwargs.items():
        setattr(instance, attr, new_val)
    commit_changes()


def delete_instance(model, id):
    model.query.filter_by(id=id).delete()
    # no Hard Deletion
    # instance = model.query.filter_by(id=id).first()
    # setattr(instance, is_active, False)
    commit_changes()