from app.repositories.leads_repository import LeadRepository
from app.repositories.sources_repository import SourceRepository
from app.repositories.operators_repository import OperatorRepository
from app.repositories.contacts_repository import ContactRepository
from app.repositories.distributions_repository import DistributionRepository


_all_repositories = [
    LeadRepository,
    SourceRepository,
    OperatorRepository,
    ContactRepository,
    DistributionRepository
]