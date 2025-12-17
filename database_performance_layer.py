"""
High-Performance Database Layer for SuitSize.ai Backend
Implements SQLite with advanced caching and optimization for production scalability
"""

import sqlite3
import json
import time
import hashlib
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """High-performance database manager with connection pooling and optimization"""
    
    def __init__(self, db_path: str = ":memory:", pool_size: int = 10):
        self.db_path = db_path
        self.pool_size = pool_size
        self.connection_pool = []
        self.lock = threading.Lock()
        self._initialize_database()
        self._create_connection_pool()
        
    def _initialize_database(self):
        """Initialize database schema and indexes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Recommendations cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recommendations_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT UNIQUE NOT NULL,
                    height REAL NOT NULL,
                    weight REAL NOT NULL,
                    fit TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    size TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    confidence_level TEXT NOT NULL,
                    body_type TEXT NOT NULL,
                    rationale TEXT NOT NULL,
                    alterations TEXT NOT NULL,
                    measurements TEXT NOT NULL,
                    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    hit_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for recommendations_cache
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_key ON recommendations_cache(cache_key)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_expires ON recommendations_cache(expires_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_last_accessed ON recommendations_cache(last_accessed)")
            
            # Performance metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint TEXT NOT NULL,
                    response_time_ms REAL NOT NULL,
                    status_code INTEGER NOT NULL,
                    cache_hit BOOLEAN NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance_metrics
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_endpoint_timestamp ON performance_metrics(endpoint, timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_response_time ON performance_metrics(response_time_ms)")
            
            # System statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT UNIQUE NOT NULL,
                    metric_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for system_stats
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metric_name ON system_stats(metric_name)")
            
            # Customer similarity cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS similarity_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    height REAL NOT NULL,
                    weight REAL NOT NULL,
                    fit TEXT NOT NULL,
                    similarity_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                )
            """)
            
            # Create indexes for similarity_cache
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_measurements ON similarity_cache(height, weight, fit)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_similarity_expires ON similarity_cache(expires_at)")
            
            conn.commit()
            logger.info("🗄️ Database schema initialized successfully")
    
    def _create_connection_pool(self):
        """Create database connection pool"""
        for _ in range(self.pool_size):
            try:
                conn = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,
                    timeout=30.0
                )
                # Optimize SQLite for performance
                conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
                conn.execute("PRAGMA synchronous=NORMAL")  # Balanced durability/performance
                conn.execute("PRAGMA cache_size=10000")  # 10MB cache
                conn.execute("PRAGMA temp_store=memory")  # In-memory temp storage
                self.connection_pool.append(conn)
            except Exception as e:
                logger.error(f"Failed to create database connection: {e}")
        
        logger.info(f"🔗 Database connection pool created with {len(self.connection_pool)} connections")
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool with automatic return"""
        conn = None
        try:
            with self.lock:
                if self.connection_pool:
                    conn = self.connection_pool.pop()
                else:
                    # Create new connection if pool is empty
                    conn = sqlite3.connect(
                        self.db_path,
                        check_same_thread=False,
                        timeout=30.0
                    )
                    conn.execute("PRAGMA journal_mode=WAL")
                    conn.execute("PRAGMA synchronous=NORMAL")
                    conn.execute("PRAGMA cache_size=10000")
                    conn.execute("PRAGMA temp_store=memory")
            
            yield conn
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                with self.lock:
                    if len(self.connection_pool) < self.pool_size:
                        self.connection_pool.append(conn)
                    else:
                        conn.close()
    
    def get_cache_key(self, height: float, weight: float, fit: str, unit: str) -> str:
        """Generate optimized cache key"""
        data = f"{height:.1f}_{weight:.1f}_{fit}_{unit}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_cached_recommendation(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached recommendation with performance tracking"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Update hit count and last accessed time
                cursor.execute("""
                    UPDATE recommendations_cache 
                    SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
                """, (cache_key,))
                
                # Fetch the cached result
                cursor.execute("""
                    SELECT size, confidence, confidence_level, body_type, 
                           rationale, alterations, measurements, hit_count
                    FROM recommendations_cache 
                    WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
                """, (cache_key,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'size': row[0],
                        'confidence': row[1],
                        'confidenceLevel': row[2],
                        'bodyType': row[3],
                        'rationale': row[4],
                        'alterations': json.loads(row[5]),
                        'measurements': json.loads(row[6]),
                        'cached': True,
                        'hit_count': row[7]
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Cache retrieval error: {e}")
            return None
    
    def cache_recommendation(self, height: float, weight: float, fit: str, unit: str,
                           recommendation: Dict[str, Any], ttl_seconds: int = 300) -> bool:
        """Cache recommendation with optimized storage"""
        try:
            cache_key = self.get_cache_key(height, weight, fit, unit)
            expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO recommendations_cache 
                    (cache_key, height, weight, fit, unit, size, confidence, 
                     confidence_level, body_type, rationale, alterations, 
                     measurements, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cache_key, height, weight, fit, unit,
                    recommendation['size'], recommendation['confidence'],
                    recommendation['confidenceLevel'], recommendation['bodyType'],
                    recommendation['rationale'], json.dumps(recommendation['alterations']),
                    json.dumps(recommendation['measurements']), expires_at.isoformat()
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Cache storage error: {e}")
            return False
    
    def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM recommendations_cache 
                    WHERE expires_at < CURRENT_TIMESTAMP
                """)
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                if deleted_count > 0:
                    logger.info(f"🧹 Cleaned up {deleted_count} expired cache entries")
                
                return deleted_count
                
        except Exception as e:
            logger.error(f"Cache cleanup error: {e}")
            return 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total cache entries
                cursor.execute("SELECT COUNT(*) FROM recommendations_cache")
                total_entries = cursor.fetchone()[0]
                
                # Active (non-expired) entries
                cursor.execute("""
                    SELECT COUNT(*) FROM recommendations_cache 
                    WHERE expires_at > CURRENT_TIMESTAMP
                """)
                active_entries = cursor.fetchone()[0]
                
                # Average hit count
                cursor.execute("""
                    SELECT AVG(hit_count) FROM recommendations_cache 
                    WHERE hit_count > 0
                """)
                avg_hits = cursor.fetchone()[0] or 0
                
                # Most accessed entries
                cursor.execute("""
                    SELECT cache_key, hit_count FROM recommendations_cache 
                    ORDER BY hit_count DESC LIMIT 5
                """)
                top_entries = cursor.fetchall()
                
                return {
                    'total_entries': total_entries,
                    'active_entries': active_entries,
                    'expired_entries': total_entries - active_entries,
                    'average_hit_count': round(avg_hits, 2),
                    'top_accessed': [{'cache_key': row[0], 'hits': row[1]} for row in top_entries]
                }
                
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {}
    
    def record_performance_metric(self, endpoint: str, response_time_ms: float, 
                                status_code: int, cache_hit: bool):
        """Record performance metric for monitoring"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO performance_metrics 
                    (endpoint, response_time_ms, status_code, cache_hit)
                    VALUES (?, ?, ?, ?)
                """, (endpoint, response_time_ms, status_code, cache_hit))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Performance metric recording error: {e}")
    
    def get_performance_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance statistics for the last N hours"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Overall stats
                cursor.execute("""
                    SELECT COUNT(*), AVG(response_time_ms), MIN(response_time_ms), 
                           MAX(response_time_ms), AVG(CASE WHEN cache_hit THEN 1.0 ELSE 0.0 END)
                    FROM performance_metrics 
                    WHERE timestamp > datetime('now', '-{} hours')
                """.format(hours))
                
                stats = cursor.fetchone()
                total_requests = stats[0] or 0
                avg_response_time = stats[1] or 0
                min_response_time = stats[2] or 0
                max_response_time = stats[3] or 0
                cache_hit_rate = stats[4] or 0
                
                # Percentiles
                cursor.execute("""
                    SELECT response_time_ms FROM performance_metrics 
                    WHERE timestamp > datetime('now', '-{} hours')
                    ORDER BY response_time_ms
                """.format(hours))
                
                response_times = [row[0] for row in cursor.fetchall()]
                
                percentiles = {}
                if response_times:
                    import numpy as np
                    percentiles = {
                        'p50': round(np.percentile(response_times, 50), 2),
                        'p95': round(np.percentile(response_times, 95), 2),
                        'p99': round(np.percentile(response_times, 99), 2)
                    }
                
                return {
                    'period_hours': hours,
                    'total_requests': total_requests,
                    'average_response_time_ms': round(avg_response_time, 2),
                    'min_response_time_ms': round(min_response_time, 2),
                    'max_response_time_ms': round(max_response_time, 2),
                    'cache_hit_rate': round(cache_hit_rate, 3),
                    'percentiles': percentiles
                }
                
        except Exception as e:
            logger.error(f"Performance stats error: {e}")
            return {}
    
    def update_system_stat(self, metric_name: str, metric_value: Any):
        """Update system statistic"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO system_stats 
                    (metric_name, metric_value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (metric_name, str(metric_value)))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"System stat update error: {e}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get all system statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT metric_name, metric_value, updated_at 
                    FROM system_stats
                """)
                
                stats = {}
                for row in cursor.fetchall():
                    stats[row[0]] = {
                        'value': row[1],
                        'updated_at': row[2]
                    }
                
                return stats
                
        except Exception as e:
            logger.error(f"System stats retrieval error: {e}")
            return {}
    
    def optimize_database(self):
        """Perform database optimization"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Vacuum to reclaim space
                cursor.execute("VACUUM")
                
                # Analyze to update statistics
                cursor.execute("ANALYZE")
                
                # Reindex for optimal performance
                cursor.execute("REINDEX")
                
                conn.commit()
                logger.info("🔧 Database optimization completed")
                
        except Exception as e:
            logger.error(f"Database optimization error: {e}")

class OptimizedCacheManager:
    """Multi-tier caching manager with database persistence"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.memory_cache = {}  # L1: In-memory cache
        self.memory_ttl = 60  # 1 minute for memory cache
        
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get from multi-tier cache (L1 memory -> L2 database)"""
        
        # L1: Check memory cache first
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if time.time() - entry['timestamp'] < self.memory_ttl:
                return entry['data']
            else:
                del self.memory_cache[cache_key]
        
        # L2: Check database cache
        db_result = self.db_manager.get_cached_recommendation(cache_key)
        if db_result:
            # Store in L1 cache for faster access
            self.memory_cache[cache_key] = {
                'data': db_result,
                'timestamp': time.time()
            }
            return db_result
        
        return None
    
    def set(self, cache_key: str, data: Dict[str, Any], ttl_seconds: int = 300):
        """Set in multi-tier cache (L1 memory -> L2 database)"""
        
        # L1: Store in memory cache
        self.memory_cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        # L2: Store in database cache
        self.db_manager.cache_recommendation(
            data.get('height', 0),
            data.get('weight', 0),
            data.get('fit', 'regular'),
            data.get('unit', 'metric'),
            data,
            ttl_seconds
        )
    
    def clear(self):
        """Clear all caches"""
        self.memory_cache.clear()
        # Database cache cleanup handled separately
        
    def get_stats(self) -> Dict[str, Any]:
        """Get multi-tier cache statistics"""
        memory_stats = {
            'memory_entries': len(self.memory_cache),
            'memory_cache_size_kb': sum(len(str(v)) for v in self.memory_cache.values()) / 1024
        }
        
        db_stats = self.db_manager.get_cache_stats()
        
        return {
            'memory_cache': memory_stats,
            'database_cache': db_stats,
            'total_cache_entries': memory_stats['memory_entries'] + db_stats.get('active_entries', 0)
        }

if __name__ == "__main__":
    # Test the database and caching system
    print("🧪 Testing Database Performance Layer")
    
    db = DatabaseManager()
    cache = OptimizedCacheManager(db)
    
    # Test caching
    test_data = {
        'height': 175,
        'weight': 75,
        'fit': 'regular',
        'unit': 'metric',
        'size': '50R',
        'confidence': 0.92,
        'confidenceLevel': 'Very High',
        'bodyType': 'Athletic',
        'rationale': 'Test recommendation',
        'alterations': ['shoulder_adjustment'],
        'measurements': {'height_cm': 175, 'weight_kg': 75}
    }
    
    cache_key = db.get_cache_key(175, 75, 'regular', 'metric')
    
    # Test set and get
    cache.set(cache_key, test_data)
    retrieved = cache.get(cache_key)
    
    print(f"✅ Cache test: {'PASSED' if retrieved else 'FAILED'}")
    print(f"📊 Cache stats: {cache.get_stats()}")
    
    # Test database performance
    print(f"\n📈 Performance stats: {db.get_performance_stats(1)}")
    print(f"💾 System stats: {db.get_system_stats()}")