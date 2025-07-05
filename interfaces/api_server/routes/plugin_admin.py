from fastapi import APIRouter, Depends
from interfaces.api_server.auth import get_current_user
from ai.plugins.plugin_registry import (
    register_plugin_intents,
    is_plugin_enabled,
    enable_plugin,
    disable_plugin,
    list_enabled_plugins,
)
"""plugin_admin.py - Plugin management routes for admin users
✅ Register plugins with intents
"""
router = APIRouter(prefix="/admin/plugins", tags=["plugin-admin"])

@router.post("/register")
async def register_plugin(
    plugin_name: str,
    intents: list,
    current_user: str = Depends(get_current_user)
):
    """
    Register a plugin for a list of intents (in-memory).
    """
    register_plugin_intents(plugin_name, intents)
    return {"plugin": plugin_name, "intents": intents}

@router.post("/enable")
async def enable_plugin_for_user(
    user_id: str,
    plugin_name: str,
    current_user: str = Depends(get_current_user)
):
    """
    Enable a plugin for a user (in-memory).
    """
    enable_plugin(user_id, plugin_name)
    return {"user_id": user_id, "plugin": plugin_name, "enabled": True}

@router.post("/disable")
async def disable_plugin_for_user(
    user_id: str,
    plugin_name: str,
    current_user: str = Depends(get_current_user)
):
    """
    Disable a plugin for a user (in-memory).
    """
    disable_plugin(user_id, plugin_name)
    return {"user_id": user_id, "plugin": plugin_name, "enabled": False}

@router.get("/enabled/{user_id}")
async def get_enabled_plugins(
    user_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    List enabled plugins for a user (in-memory).
    """
    plugins = list_enabled_plugins(user_id)
    return {"user_id": user_id, "enabled_plugins": plugins}

@router.get("/is-enabled")
async def check_plugin_enabled(
    user_id: str,
    plugin_name: str,
    current_user: str = Depends(get_current_user)
):
    """
    Check if a plugin is enabled for a user (in-memory).
    """
    enabled = is_plugin_enabled(user_id, plugin_name)
    return {"user_id": user_id, "plugin": plugin_name, "enabled": enabled}