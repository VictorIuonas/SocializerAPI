from typing import List

from api import db
from connected.db_models import Connection, Organization
from connected.entities import DevsConnection, OrganizationEntity


class ConnectionsRepository:

    def add_connection_between_developers(
            self, dev1: str, dev2: str, are_connected: bool, common_organizations: List[OrganizationEntity]
    ) -> DevsConnection:
        db_organizations = self.get_or_create_organizations(common_organizations)

        db_connection = Connection(dev1=dev1, dev2=dev2, are_linked=are_connected)
        for db_organization in db_organizations:
            db_connection.common_organizations.append(db_organization)
        db.session.add(db_connection)
        db.session.commit()

        return self.to_connection_domain(db_connection)

    def get_connection_for_developers(self, dev1: str, dev2: str):
        db_connections = Connection.query.filter_by(dev1=dev1, dev2=dev2)
        return [self.to_connection_domain(connection) for connection in db_connections]

    def to_connection_domain(self, connection: Connection) -> DevsConnection:
        return DevsConnection(
            timestamp=connection.timestamp, connected=connection.are_linked,
            organizations=[self.to_organization_domain(org) for org in connection.common_organizations]
        )

    @staticmethod
    def to_organization_domain(organization: Organization):
        return OrganizationEntity(id=organization.id, name=organization.name, external_id=organization.external_id)

    @staticmethod
    def get_or_create_organizations(organizations: List[OrganizationEntity]) -> List[Organization]:
        result = []

        for organization in organizations:
            db_organization = Organization.query.filter_by(external_id=organization.external_id).first()
            if not db_organization:
                db_organization = Organization(name=organization.name, external_id=organization.external_id)
                db.session.add(db_organization)
                db.session.commit()

            result.append(db_organization)

        return result
