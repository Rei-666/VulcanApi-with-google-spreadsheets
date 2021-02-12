def merge_all(session, table, object_list):
    for instance in object_list:
        is_in_db = bool(session.query(table).filter(table.id == instance.id).first())
        if not is_in_db:
            session.add(instance)
