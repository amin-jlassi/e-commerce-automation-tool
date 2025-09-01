def to_dict(row) :  
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}