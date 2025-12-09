from app.api.routers.sources_routes import router as router_sources
from app.api.routers.contacts_routes import router as router_contacts
from app.api.routers.operators_routes import router as router_operators
from app.api.routers.distributions_routes import router as router_distributions


routers = [router_sources, router_contacts, router_operators, router_distributions]