from datetime import datetime

from sqlalchemy.orm import relationship

from api import db


class Organization(db.Model):
    __tablename__ = "organizations"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    external_id = db.Column(db.Integer)


class Connection(db.Model):
    __tablename__ = "connections"
    __table_args__ = (
        db.UniqueConstraint('dev1', 'dev2', 'timestamp', name='_devs_timestamp_uc'),
        {'extend_existing': True}
    )
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    dev1 = db.Column(db.String(100))
    dev2 = db.Column(db.String(100))
    are_linked = db.Column(db.Boolean)

    common_organizations = relationship(
        Organization, secondary='connection_x_organization_table', lazy='subquery',
        backref=db.backref('connections', lazy=True)
    )


ConnectionsToOrganizations = db.Table(
    'connection_x_organization_table',
    db.Column('connections_id', db.Integer, db.ForeignKey('connections.id'), primary_key=True),
    db.Column('organizations_id', db.Integer, db.ForeignKey('organizations.id'), primary_key=True),
    extend_existing=True
)
