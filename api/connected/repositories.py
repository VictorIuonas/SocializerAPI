from connected.db_models import Connection, Organization
from connected.entities import DevsConnection, OrganizationEntity


class ConnectionsRepository:

    def get_connection_for_developers(self, dev1, dev2):
        db_connections = Connection.query.filter_by(dev1=dev1, dev2=dev2)
        return [self.to_connection_domain(connection) for connection in db_connections]

    def to_connection_domain(self, connection: Connection) -> DevsConnection:
        return DevsConnection(
            timestamp=connection.timestamp, connected=connection.are_linked,
            organizations=[self.to_organization_domain(org) for org in connection.common_organizations]
        )

    @staticmethod
    def to_organization_domain(organization: Organization):
        return OrganizationEntity(id=organization.id, name=organization.name)
