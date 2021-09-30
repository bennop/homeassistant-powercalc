from __future__ import annotations

import logging

from homeassistant.core import callback

from homeassistant.helpers.entity_registry import (
    EntityRegistry,
    RegistryEntry,
    async_entries_for_device,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@callback
def async_migrate_unique_id(
    ent_reg: EntityRegistry, platform: str, old_unique_id: str, new_unique_id: str
) -> None:
    """Check if entity with old unique ID exists, and if so migrate it to new ID."""
    if entity_id := ent_reg.async_get_entity_id(platform, DOMAIN, old_unique_id):
        _LOGGER.debug(
            "Migrating entity %s from old unique ID '%s' to new unique ID '%s'",
            entity_id,
            old_unique_id,
            new_unique_id,
        )
        try:
            ent_reg.async_update_entity(entity_id, new_unique_id=new_unique_id)
        except ValueError:
            _LOGGER.debug(
                (
                    "Entity %s can't be migrated because the unique ID is taken; "
                    "Cleaning it up since it is likely no longer valid"
                ),
                entity_id,
            )
            ent_reg.async_remove(entity_id)
        
@callback
def async_migrate_entity_id(
    ent_reg: EntityRegistry, platform: str, unique_id: str, new_entity_id: str
) -> None:
    """Check if entity with old unique ID exists, and if so migrate it to new ID."""

    existing_entity_id = ent_reg.async_get_entity_id(platform, DOMAIN, unique_id)
    if existing_entity_id is None or existing_entity_id == new_entity_id:
        return
    
    _LOGGER.debug(
        "Migrating entity from old entity ID '%s' to new entity ID '%s'",
        existing_entity_id,
        new_entity_id,
    )
    try:
        ent_reg.async_update_entity(existing_entity_id, new_entity_id=new_entity_id)
    except ValueError as e:
        _LOGGER.error(
            e
        )
        ent_reg.async_remove(new_entity_id)