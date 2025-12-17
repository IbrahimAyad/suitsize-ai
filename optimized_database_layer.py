"""
Simplified High-Performance Database Layer for SuitSize.ai Backend
Focus on reliability and performance
"""

import sqlite3
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SimpleDatabaseManager:
    """Simplified but high-performance database manager"""
    
    def __init__(self, db_path: str = "suitsize_cache.db"):
        self.db_path = db_path
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
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
            
            # Create indexes
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
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metric_name ON system_stats(metric_name)")
            
            conn.commit()
            logger.info("🗄️ Database schema initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
        finally:
            conn.close()
    
    def get_cache_key(self, height: float, weight: float, fit: str, unit: str) -> str:
        """Generate optimized cache key"""
        data = f"{height:.1f}_{weight:.1f}_{fit}_{unit}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_cached_recommendation(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached recommendation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Update hit count
            cursor.execute("""
                UPDATE recommendations_cache 
                SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP
                WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
            """, (cache_key,))
            
            # Fetch result
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
        finally:
            conn.close()
    
    def cache_recommendation(self, height: float, weight: float, fit: str, unit: str,
                           recommendation: Dict[str, Any], ttl_seconds: int = 300) -> bool:
        """Cache recommendation"""
        cache_key = self.get_cache_key(height, weight, fit, unit)
        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
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
        finally:
            conn.close()
    
    def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
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
        finally:
            conn.close()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total entries
            cursor.execute("SELECT COUNT(*) FROM recommendations_cache")
            total_entries = cursor.fetchone()[0]
            
            # Active entries
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
            
            return {
                'total_entries': total_entries,
                'active_entries': active_entries,
                'expired_entries': total_entries - active_entries,
                'average_hit_count': round(avg_hits, 2)
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {}
        finally:
            conn.close()
    
    def record_performance_metric(self, endpoint: str, response_time_ms: float, 
                                status_code: int, cache_hit: bool):
        """Record performance metric"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO performance_metrics 
                (endpoint, response_time_ms, status_code, cache_hit)
                VALUES (?, ?, ?, ?)
            """, (endpoint, response_time_ms, status_code, cache_hit))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Performance metric recording error: {e}")
        finally:
            conn.close()
    
    def get_performance_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT COUNT(*), AVG(response_time_ms), MIN(response_time_ms), 
                       MAX(response_time_ms), AVG(CASE WHEN cache_hit THEN 1.0 ELSE 0.0 END)
                FROM performance_metrics 
                WHERE timestamp > datetime('now', '-{} hours')
            """.format(hours))
            
            stats = cursor.fetchone()
            if stats and stats[0] > 0:
                return {
                    'period_hours': hours,
                    'total_requests': stats[0],
                    'average_response_time_ms': round(stats[1], 2),
                    'min_response_time_ms': round(stats[2], 2),
                    'max_response_time_ms': round(stats[3], 2),
                    'cache_hit_rate': round(stats[4], 3)
                }
            return {}
            
        except Exception as e:
            logger.error(f"Performance stats error: {e}")
            return {}
        finally:
            conn.close()

class OptimizedPerformanceBackend:
    """Enhanced backend with database optimization and performance monitoring"""
    
    def __init__(self, db_manager: SimpleDatabaseManager):
        self.db_manager = db_manager
        self.memory_cache = {}  # L1: Fast in-memory cache
        self.memory_ttl = 30  # 30 seconds for memory cache
        
    def get_cache_key(self, height: float, weight: float, fit: str, unit: str) -> str:
        """Generate cache key"""
        return self.db_manager.get_cache_key(height, weight, fit, unit)
    
    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get from multi-tier cache"""
        
        # L1: Memory cache
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if time.time() - entry['timestamp'] < self.memory_ttl:
                return entry['data']
            else:
                del self.memory_cache[cache_key]
        
        # L2: Database cache
        db_result = self.db_manager.get_cached_recommendation(cache_key)
        if db_result:
            # Store in memory for faster access
            self.memory_cache[cache_key] = {
                'data': db_result,
                'timestamp': time.time()
            }
            return db_result
        
        return None
    
    def set(self, cache_key: str, data: Dict[str, Any], ttl_seconds: int = 300):
        """Set in multi-tier cache"""
        
        # L1: Memory cache
        self.memory_cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        # L2: Database cache
        self.db_manager.cache_recommendation(
            data.get('height', 0),
            data.get('weight', 0),
            data.get('fit', 'regular'),
            data.get('unit', 'metric'),
            data,
            ttl_seconds
        )
    
    def record_request(self, endpoint: str, response_time_ms: float, 
                      status_code: int, cache_hit: bool):
        """Record request performance"""
        self.db_manager.record_performance_metric(
            endpoint, response_time_ms, status_code, cache_hit
        )
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        cache_stats = self.db_manager.get_cache_stats()
        perf_stats = self.db_manager.get_performance_stats(1)  # Last hour
        
        return {
            'cache_performance': cache_stats,
            'request_performance': perf_stats,
            'memory_cache': {
                'entries': len(self.memory_cache),
                'size_kb': sum(len(str(v)) for v in self.memory_cache.values()) / 1024
            }
        }

# Test the optimized system
if __name__ == "__main__":
    print("🚀 Testing Optimized Performance Backend")
    
    # Initialize database and cache
    db = SimpleDatabaseManager(":memory:")
    backend = OptimizedPerformanceBackend(db)
    
    # Test data
    test_data = {
        'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric',
        'size': '50R', 'confidence': 0.92, 'confidenceLevel': 'Very High',
        'bodyType': 'Athletic', 'rationale': 'Test recommendation',
        'alterations': ['shoulder_adjustment'],
        'measurements': {'height_cm': 175, 'weight_kg': 75}
    }
    
    cache_key = backend.get_cache_key(175, 75, 'regular', 'metric')
    
    # Test caching performance
    start_time = time.time()
    
    # First request (cache miss)
    backend.set(cache_key, test_data)
    result1 = backend.get(cache_key)
    
    # Second request (cache hit)
    result2 = backend.get(cache_key)
    
    # Record performance
    backend.record_request('/api/recommend', 5.2, 200, True)
    
    end_time = time.time()
    
    print(f"✅ Cache test: {'PASSED' if result1 and result2 else 'FAILED'}")
    print(f"⚡ Performance: {(end_time - start_time) * 1000:.2f}ms")
    print(f"📊 Cache stats: {backend.get_performance_report()}")
    
    # Test database performance
    print(f"\n💾 Database performance stats: {db.get_performance_stats(1)}")