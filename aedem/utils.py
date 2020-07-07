def dictionarize(row) -> dict:
    """Transform SQLAlchemy objects into dicts"""
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())
