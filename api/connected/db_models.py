from datetime import datetime

from sqlalchemy.orm import relationship, backref

from api import db


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    external_id = db.Column(db.Integer)

    connections = relationship('Connection', secondary='link_connections_organizations')


class Connection(db.Model):
    __tablename__ = 'connections'

    id = db.Column(db.Integer, primary_key=True)
    dev1 = db.Column(db.String(100))
    dev2 = db.Column(db.String(100))

    is_twitter_link = db.Column(db.Boolean)
    organizations = relationship('Organization', secondary='link_connections_organizations')


class ConnectionToOrganization(db.Model):
    __tablename__ = 'link_connections_organizations'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    connection_id = db.Column(db.Integer, db.ForeignKey('connections.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    connection = relationship(
        Connection, backref=backref('link_connections_organizations', cascade='all, delete-orphan')
    )
    organization = relationship(
        Organization, backref=backref('link_connections_organizations', cascade='all, delete-orphan')
    )
