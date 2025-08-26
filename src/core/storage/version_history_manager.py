"""
Version History Manager for Phase 2 Implementation
Maintains version history for all intelligence data with change detection,
version comparison, and rollback capabilities.
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import difflib

from ..database_manager import DatabaseManager


class VersionStatus(Enum):
    """Version status types."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    ROLLED_BACK = "rolled_back"


@dataclass
class Version:
    """Version record for intelligence data."""
    version_id: str
    content_id: str
    version_number: int
    content_hash: str
    content: Any
    metadata: Dict[str, Any]
    created_at: datetime
    created_by: str
    status: VersionStatus
    parent_version_id: Optional[str] = None
    change_summary: Optional[str] = None
    change_type: Optional[str] = None
    rollback_count: int = 0


@dataclass
class DiffResult:
    """Result of version comparison."""
    version1_id: str
    version2_id: str
    differences: List[Dict[str, Any]]
    similarity_score: float
    change_count: int
    added_content: List[str]
    removed_content: List[str]
    modified_content: List[str]


@dataclass
class VersionHistory:
    """Version history for a content item."""
    content_id: str
    versions: List[Version]
    current_version: Version
    total_versions: int
    first_version_date: datetime
    last_version_date: datetime
    change_frequency: float  # Changes per day


class VersionHistoryManager:
    """Version history manager for intelligence data."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize database manager
        self.database_manager = DatabaseManager(config.get("database", {}))
        
        # Version tracking
        self.version_cache = {}
        self.cache_ttl = config.get("version_cache_ttl", 1800)  # 30 minutes
        
        # Retention policy
        self.retention_days = config.get("retention_days", 365)
        self.max_versions_per_content = config.get("max_versions_per_content", 50)
        
        # Change detection settings
        self.change_threshold = config.get("change_threshold", 0.1)  # 10% change threshold
        self.similarity_threshold = config.get("similarity_threshold", 0.8)
    
    async def create_version(self, content: Any, metadata: Dict[str, Any], 
                           content_id: Optional[str] = None, 
                           user_id: Optional[str] = None) -> str:
        """Create a new version of content."""
        try:
            # Generate content ID if not provided
            if content_id is None:
                content_id = self._generate_content_id(content)
            
            # Generate content hash
            content_hash = self._generate_content_hash(content)
            
            # Check if this is a significant change
            current_version = await self._get_current_version(content_id)
            if current_version:
                similarity = self._calculate_similarity(content, current_version.content)
                if similarity > self.similarity_threshold:
                    self.logger.info(f"Content change too small to create new version (similarity: {similarity})")
                    return current_version.version_id
            
            # Get next version number
            version_number = await self._get_next_version_number(content_id)
            
            # Create version record
            version = Version(
                version_id=str(uuid.uuid4()),
                content_id=content_id,
                version_number=version_number,
                content_hash=content_hash,
                content=content,
                metadata=metadata,
                created_at=datetime.now(),
                created_by=user_id or "system",
                status=VersionStatus.ACTIVE,
                parent_version_id=current_version.version_id if current_version else None,
                change_summary=await self._generate_change_summary(content, current_version),
                change_type=await self._determine_change_type(content, current_version)
            )
            
            # Store version in database
            await self._store_version(version)
            
            # Update cache
            self._update_version_cache(content_id, version)
            
            # Cleanup old versions if needed
            await self._cleanup_old_versions(content_id)
            
            self.logger.info(f"Created version {version_number} for content {content_id}")
            return version.version_id
            
        except Exception as e:
            self.logger.error(f"Failed to create version: {e}")
            raise
    
    async def get_version_history(self, content_id: str) -> VersionHistory:
        """Get version history for a content item."""
        try:
            # Check cache first
            if content_id in self.version_cache:
                cache_entry = self.version_cache[content_id]
                if datetime.now() - cache_entry["timestamp"] < timedelta(seconds=self.cache_ttl):
                    return cache_entry["history"]
            
            # Get versions from database
            versions = await self._get_versions_from_db(content_id)
            
            if not versions:
                raise ValueError(f"No versions found for content_id: {content_id}")
            
            # Sort versions by version number
            versions.sort(key=lambda v: v.version_number)
            
            # Get current version (latest active version)
            current_version = next((v for v in reversed(versions) if v.status == VersionStatus.ACTIVE), versions[-1])
            
            # Calculate change frequency
            if len(versions) > 1:
                first_date = versions[0].created_at
                last_date = versions[-1].created_at
                days_diff = (last_date - first_date).days
                change_frequency = len(versions) / max(days_diff, 1)
            else:
                change_frequency = 0.0
            
            # Create version history
            history = VersionHistory(
                content_id=content_id,
                versions=versions,
                current_version=current_version,
                total_versions=len(versions),
                first_version_date=versions[0].created_at,
                last_version_date=versions[-1].created_at,
                change_frequency=change_frequency
            )
            
            # Update cache
            self._update_version_cache(content_id, history)
            
            return history
            
        except Exception as e:
            self.logger.error(f"Failed to get version history: {e}")
            raise
    
    async def compare_versions(self, version1_id: str, version2_id: str) -> DiffResult:
        """Compare two versions of content."""
        try:
            # Get versions
            version1 = await self._get_version_by_id(version1_id)
            version2 = await self._get_version_by_id(version2_id)
            
            if not version1 or not version2:
                raise ValueError("One or both versions not found")
            
            # Calculate similarity
            similarity = self._calculate_similarity(version1.content, version2.content)
            
            # Generate differences
            differences = self._generate_differences(version1.content, version2.content)
            
            # Categorize changes
            added_content = []
            removed_content = []
            modified_content = []
            
            for diff in differences:
                if diff["type"] == "added":
                    added_content.append(diff["content"])
                elif diff["type"] == "removed":
                    removed_content.append(diff["content"])
                elif diff["type"] == "modified":
                    modified_content.append(diff["content"])
            
            return DiffResult(
                version1_id=version1_id,
                version2_id=version2_id,
                differences=differences,
                similarity_score=similarity,
                change_count=len(differences),
                added_content=added_content,
                removed_content=removed_content,
                modified_content=modified_content
            )
            
        except Exception as e:
            self.logger.error(f"Failed to compare versions: {e}")
            raise
    
    async def rollback_to_version(self, content_id: str, version_id: str) -> bool:
        """Rollback content to a specific version."""
        try:
            # Get target version
            target_version = await self._get_version_by_id(version_id)
            if not target_version or target_version.content_id != content_id:
                raise ValueError("Target version not found or doesn't match content_id")
            
            # Get current version
            current_version = await self._get_current_version(content_id)
            if not current_version:
                raise ValueError("No current version found")
            
            # Create new version with rollback content
            rollback_metadata = {
                "rollback_from": current_version.version_id,
                "rollback_to": version_id,
                "rollback_reason": "User requested rollback",
                "original_content": current_version.content
            }
            
            # Create rollback version
            rollback_version_id = await self.create_version(
                content=target_version.content,
                metadata=rollback_metadata,
                content_id=content_id,
                user_id="system_rollback"
            )
            
            # Update rollback count
            target_version.rollback_count += 1
            await self._update_version(target_version)
            
            self.logger.info(f"Successfully rolled back content {content_id} to version {version_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to rollback to version: {e}")
            return False
    
    async def cleanup_old_versions(self, retention_days: Optional[int] = None) -> int:
        """Clean up old versions based on retention policy."""
        try:
            days = retention_days or self.retention_days
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get old versions
            old_versions = await self._get_old_versions(cutoff_date)
            
            # Archive old versions
            archived_count = 0
            for version in old_versions:
                if version.status == VersionStatus.ACTIVE:
                    version.status = VersionStatus.ARCHIVED
                    await self._update_version(version)
                    archived_count += 1
            
            # Clean up cache
            self._cleanup_version_cache()
            
            self.logger.info(f"Archived {archived_count} old versions")
            return archived_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old versions: {e}")
            return 0
    
    async def get_version_metadata(self, version_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific version."""
        try:
            version = await self._get_version_by_id(version_id)
            if version:
                return {
                    "version_id": version.version_id,
                    "content_id": version.content_id,
                    "version_number": version.version_number,
                    "content_hash": version.content_hash,
                    "created_at": version.created_at.isoformat(),
                    "created_by": version.created_by,
                    "status": version.status.value,
                    "parent_version_id": version.parent_version_id,
                    "change_summary": version.change_summary,
                    "change_type": version.change_type,
                    "rollback_count": version.rollback_count,
                    "metadata": version.metadata
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get version metadata: {e}")
            return None
    
    def _generate_content_id(self, content: Any) -> str:
        """Generate a unique content ID."""
        content_str = str(content)
        return hashlib.sha256(content_str.encode()).hexdigest()[:16]
    
    def _generate_content_hash(self, content: Any) -> str:
        """Generate hash for content."""
        content_str = str(content)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def _calculate_similarity(self, content1: Any, content2: Any) -> float:
        """Calculate similarity between two content items."""
        try:
            str1 = str(content1)
            str2 = str(content2)
            
            # Use difflib for similarity calculation
            similarity = difflib.SequenceMatcher(None, str1, str2).ratio()
            return similarity
            
        except Exception as e:
            self.logger.error(f"Failed to calculate similarity: {e}")
            return 0.0
    
    def _generate_differences(self, content1: Any, content2: Any) -> List[Dict[str, Any]]:
        """Generate differences between two content items."""
        differences = []
        
        try:
            str1 = str(content1)
            str2 = str(content2)
            
            # Use difflib to generate differences
            diff = difflib.unified_diff(
                str1.splitlines(keepends=True),
                str2.splitlines(keepends=True),
                lineterm=''
            )
            
            for line in diff:
                if line.startswith('+') and not line.startswith('+++'):
                    differences.append({
                        "type": "added",
                        "content": line[1:].strip(),
                        "line": line
                    })
                elif line.startswith('-') and not line.startswith('---'):
                    differences.append({
                        "type": "removed",
                        "content": line[1:].strip(),
                        "line": line
                    })
                elif line.startswith(' '):
                    differences.append({
                        "type": "unchanged",
                        "content": line[1:].strip(),
                        "line": line
                    })
            
        except Exception as e:
            self.logger.error(f"Failed to generate differences: {e}")
        
        return differences
    
    async def _get_current_version(self, content_id: str) -> Optional[Version]:
        """Get the current (latest active) version of content."""
        try:
            # This would query the database for the latest active version
            # For now, return None as placeholder
            return None
        except Exception as e:
            self.logger.error(f"Failed to get current version: {e}")
            return None
    
    async def _get_next_version_number(self, content_id: str) -> int:
        """Get the next version number for content."""
        try:
            # This would query the database for the highest version number
            # For now, return 1 as placeholder
            return 1
        except Exception as e:
            self.logger.error(f"Failed to get next version number: {e}")
            return 1
    
    async def _generate_change_summary(self, new_content: Any, old_version: Optional[Version]) -> str:
        """Generate a summary of changes."""
        if not old_version:
            return "Initial version"
        
        try:
            similarity = self._calculate_similarity(new_content, old_version.content)
            if similarity < 0.5:
                return "Major content change"
            elif similarity < 0.8:
                return "Moderate content change"
            else:
                return "Minor content change"
        except Exception as e:
            self.logger.error(f"Failed to generate change summary: {e}")
            return "Content change"
    
    async def _determine_change_type(self, new_content: Any, old_version: Optional[Version]) -> str:
        """Determine the type of change."""
        if not old_version:
            return "creation"
        
        try:
            similarity = self._calculate_similarity(new_content, old_version.content)
            if similarity < 0.5:
                return "major_update"
            elif similarity < 0.8:
                return "moderate_update"
            else:
                return "minor_update"
        except Exception as e:
            self.logger.error(f"Failed to determine change type: {e}")
            return "update"
    
    async def _store_version(self, version: Version) -> None:
        """Store version in database."""
        try:
            # This would store the version in the database
            # For now, just log the operation
            self.logger.debug(f"Storing version {version.version_id} in database")
        except Exception as e:
            self.logger.error(f"Failed to store version: {e}")
            raise
    
    async def _get_versions_from_db(self, content_id: str) -> List[Version]:
        """Get all versions for content from database."""
        try:
            # This would query the database for all versions
            # For now, return empty list as placeholder
            return []
        except Exception as e:
            self.logger.error(f"Failed to get versions from database: {e}")
            return []
    
    async def _get_version_by_id(self, version_id: str) -> Optional[Version]:
        """Get version by ID from database."""
        try:
            # This would query the database for the specific version
            # For now, return None as placeholder
            return None
        except Exception as e:
            self.logger.error(f"Failed to get version by ID: {e}")
            return None
    
    async def _update_version(self, version: Version) -> None:
        """Update version in database."""
        try:
            # This would update the version in the database
            # For now, just log the operation
            self.logger.debug(f"Updating version {version.version_id} in database")
        except Exception as e:
            self.logger.error(f"Failed to update version: {e}")
            raise
    
    async def _get_old_versions(self, cutoff_date: datetime) -> List[Version]:
        """Get old versions before cutoff date."""
        try:
            # This would query the database for old versions
            # For now, return empty list as placeholder
            return []
        except Exception as e:
            self.logger.error(f"Failed to get old versions: {e}")
            return []
    
    def _update_version_cache(self, content_id: str, data: Any) -> None:
        """Update version cache."""
        self.version_cache[content_id] = {
            "data": data,
            "timestamp": datetime.now()
        }
    
    def _cleanup_version_cache(self) -> None:
        """Clean up expired entries from version cache."""
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self.version_cache.items():
            if current_time - entry["timestamp"] > timedelta(seconds=self.cache_ttl):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.version_cache[key]
        
        if expired_keys:
            self.logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
