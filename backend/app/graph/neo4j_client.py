import os
import logging
from typing import Dict, Any, List
from neo4j import GraphDatabase, exceptions

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.enabled = False

        if self.uri and self.user and self.password:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                # Optional: you can verify connectivity here, but avoid blocking if DB is down.
                # self.driver.verify_connectivity()
                self.enabled = True
                logger.info("Neo4j client initialized successfully.")
            except exceptions.ServiceUnavailable:
                logger.warning("Neo4j service unavailable. Graph functionality will be disabled.")
            except Exception as e:
                logger.error(f"Failed to initialize Neo4j client: {e}")
        else:
            logger.info("Neo4j credentials not provided. Graph functionality is disabled.")

    def close(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query: str, parameters: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        if not self.enabled or not self.driver:
            logger.debug("Graph query skipped. Neo4j is disabled or driver is not initialized.")
            return []
            
        parameters = parameters or {}
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Error executing Cypher query: {e}")
            return []

# Usage example (will be initialized in a dependency injection module)
# neo4j_client = Neo4jClient(settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
