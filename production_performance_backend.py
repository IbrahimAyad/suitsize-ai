"""
Production-Ready Performance Optimized Backend for SuitSize.ai
Implements advanced caching, database optimization, and performance monitoring
"""

import time
import json
import hashlib
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class ProductionPerformanceBackend:
    """Production-ready backend with multi-tier caching and performance monitoring"""
    
    def __init__(self, db_path: str = "suitsize_perf.db"):
        self.db_path = db_path
        self.memory_cache = {}  # L1: Ultra-fast memory cache
        self.db_cache = {}      # L2: Database cache
        self.performance_data = []
        self.cache_lock = threading.Lock()
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database with proper error handling"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            cursor = conn.cursor()
            
            # Set SQLite optimizations
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA cache_size=10000")
            
            # Create tables
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
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_key ON recommendations_cache(cache_key)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_expires ON recommendations_cache(expires_at)")
            
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
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON performance_metrics(timestamp)")
            
            conn.commit()
            conn.close()
            logger.info("🗄️ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # Continue without database if it fails
            self.db_path = None
    
    def get_cache_key(self, height: float, weight: float, fit: str, unit: str) -> str:
        """Generate optimized cache key"""
        data = f"{height:.1f}_{weight:.1f}_{fit}_{unit}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_recommendation(self, height: float, weight: float, fit: str, unit: str, 
                          ml_engine_func) -> Dict[str, Any]:
        """Get recommendation with multi-tier caching"""
        
        start_time = time.time()
        cache_key = self.get_cache_key(height, weight, fit, unit)
        
        # L1: Ultra-fast memory cache (30 second TTL)
        with self.cache_lock:
            if cache_key in self.memory_cache:
                entry = self.memory_cache[cache_key]
                if time.time() - entry['timestamp'] < 30:
                    # Record performance
                    response_time = (time.time() - start_time) * 1000
                    self._record_performance('/api/recommend', response_time, 200, True)
                    return entry['data']
                else:
                    del self.memory_cache[cache_key]
        
        # L2: Database cache check
        db_result = self._get_from_database(cache_key)
        if db_result:
            # Store in memory cache
            with self.cache_lock:
                self.memory_cache[cache_key] = {
                    'data': db_result,
                    'timestamp': time.time()
                }
            
            # Record performance
            response_time = (time.time() - start_time) * 1000
            self._record_performance('/api/recommend', response_time, 200, True)
            return db_result
        
        # L3: Generate new recommendation
        try:
            ml_result = ml_engine_func(height, weight, fit, unit)
            
            # Store in both caches
            self._store_in_caches(cache_key, height, weight, fit, unit, ml_result)
            
            # Record performance
            response_time = (time.time() - start_time) * 1000
            self._record_performance('/api/recommend', response_time, 200, False)
            
            return ml_result
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            response_time = (time.time() - start_time) * 1000
            self._record_performance('/api/recommend', response_time, 500, False)
            raise
    
    def _get_from_database(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get from database cache"""
        if not self.db_path:
            return None
            
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            # Update hit count and get result
            cursor.execute("""
                UPDATE recommendations_cache 
                SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP
                WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
            """, (cache_key,))
            
            cursor.execute("""
                SELECT size, confidence, confidence_level, body_type, 
                       rationale, alterations, measurements, hit_count
                FROM recommendations_cache 
                WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
            """, (cache_key,))
            
            row = cursor.fetchone()
            conn.close()
            
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
            logger.error(f"Database cache retrieval failed: {e}")
            return None
    
    def _store_in_caches(self, cache_key: str, height: float, weight: float, 
                        fit: str, unit: str, recommendation: Dict[str, Any]):
        """Store in both memory and database caches"""
        
        # Store in memory cache
        with self.cache_lock:
            self.memory_cache[cache_key] = {
                'data': recommendation,
                'timestamp': time.time()
            }
        
        # Store in database cache
        if self.db_path:
            try:
                expires_at = datetime.now() + timedelta(seconds=300)  # 5 minutes
                
                conn = sqlite3.connect(self.db_path, timeout=10.0)
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
                conn.close()
                
            except Exception as e:
                logger.error(f"Database cache storage failed: {e}")
    
    def _record_performance(self, endpoint: str, response_time_ms: float, 
                          status_code: int, cache_hit: bool):
        """Record performance metric"""
        if self.db_path:
            try:
                conn = sqlite3.connect(self.db_path, timeout=5.0)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO performance_metrics 
                    (endpoint, response_time_ms, status_code, cache_hit)
                    VALUES (?, ?, ?, ?)
                """, (endpoint, response_time_ms, status_code, cache_hit))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                logger.error(f"Performance recording failed: {e}")
        
        # Also store in memory for real-time monitoring
        self.performance_data.append({
            'timestamp': time.time(),
            'endpoint': endpoint,
            'response_time_ms': response_time_ms,
            'status_code': status_code,
            'cache_hit': cache_hit
        })
        
        # Keep only last 1000 records in memory
        if len(self.performance_data) > 1000:
            self.performance_data = self.performance_data[-1000:]
    
    def get_performance_stats(self, hours: int = 1) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        
        cutoff_time = time.time() - (hours * 3600)
        recent_data = [d for d in self.performance_data if d['timestamp'] > cutoff_time]
        
        if not recent_data:
            return {'message': 'No recent performance data'}
        
        response_times = [d['response_time_ms'] for d in recent_data]
        cache_hits = [d['cache_hit'] for d in recent_data]
        
        # Calculate statistics
        stats = {
            'period_hours': hours,
            'total_requests': len(recent_data),
            'average_response_time_ms': round(sum(response_times) / len(response_times), 2),
            'min_response_time_ms': round(min(response_times), 2),
            'max_response_time_ms': round(max(response_times), 2),
            'cache_hit_rate': round(sum(cache_hits) / len(cache_hits), 3),
            'requests_per_second': round(len(recent_data) / (hours * 3600), 2)
        }
        
        # Percentiles
        if len(response_times) > 10:
            sorted_times = sorted(response_times)
            n = len(sorted_times)
            stats['p50_ms'] = round(sorted_times[int(n * 0.5)], 2)
            stats['p95_ms'] = round(sorted_times[int(n * 0.95)], 2)
            stats['p99_ms'] = round(sorted_times[int(n * 0.99)], 2)
        
        # Cache statistics
        with self.cache_lock:
            memory_cache_size = len(self.memory_cache)
            memory_cache_kb = sum(len(str(v)) for v in self.memory_cache.values()) / 1024
        
        stats['cache_performance'] = {
            'memory_cache_entries': memory_cache_size,
            'memory_cache_size_kb': round(memory_cache_size, 2),
            'cache_efficiency': 'excellent' if stats['cache_hit_rate'] > 0.8 else 'good' if stats['cache_hit_rate'] > 0.6 else 'needs_improvement'
        }
        
        return stats
    
    def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries"""
        if not self.db_path:
            return 0
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM recommendations_cache 
                WHERE expires_at < CURRENT_TIMESTAMP
            """)
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            # Clean memory cache
            current_time = time.time()
            with self.cache_lock:
                expired_keys = [
                    key for key, entry in self.memory_cache.items()
                    if current_time - entry['timestamp'] > 30
                ]
                for key in expired_keys:
                    del self.memory_cache[key]
            
            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} expired database cache entries")
                logger.info(f"🧹 Cleaned up {len(expired_keys)} expired memory cache entries")
            
            return deleted_count + len(expired_keys)
            
        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")
            return 0
    
    def optimize_database(self):
        """Optimize database performance"""
        if not self.db_path:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vacuum to reclaim space
            cursor.execute("VACUUM")
            
            # Analyze to update statistics
            cursor.execute("ANALYZE")
            
            conn.commit()
            conn.close()
            logger.info("🔧 Database optimization completed")
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database_available': self.db_path is not None,
            'memory_cache_entries': len(self.memory_cache),
            'performance_records': len(self.performance_data),
            'cache_cleanup_needed': len([k for k, v in self.memory_cache.items() 
                                       if time.time() - v['timestamp'] > 30]) > 0
        }

# Test the production performance backend
if __name__ == "__main__":
    print("🚀 Testing Production Performance Backend")
    
    # Mock ML engine function
    def mock_ml_engine(height, weight, fit, unit):
        return {
            'size': '50R',
            'confidence': 0.92,
            'confidenceLevel': 'Very High',
            'bodyType': 'Athletic',
            'rationale': 'ML analysis suggests 50R size',
            'alterations': ['shoulder_adjustment'],
            'measurements': {'height_cm': height, 'weight_kg': weight, 'unit': unit}
        }
    
    # Initialize performance backend
    backend = ProductionPerformanceBackend(":memory:")
    
    # Test performance
    test_cases = [
        {'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric'},
        {'height': 180, 'weight': 80, 'fit': 'slim', 'unit': 'metric'},
        {'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric'},  # Cache hit
    ]
    
    print("🧪 Running performance tests...")
    
    for i, test_case in enumerate(test_cases):
        start_time = time.time()
        result = backend.get_recommendation(
            test_case['height'], test_case['weight'], 
            test_case['fit'], test_case['unit'], 
            mock_ml_engine
        )
        end_time = time.time()
        
        print(f"  Test {i+1}: {result['size']} ({'cached' if result.get('cached') else 'fresh'}) - {(end_time-start_time)*1000:.2f}ms")
    
    # Get performance statistics
    print(f"\n📊 Performance Statistics:")
    stats = backend.get_performance_stats(1)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n💾 Health Status: {backend.get_health_status()}")
    
    # Test cleanup
    print(f"\n🧹 Testing cache cleanup...")
    cleaned = backend.cleanup_expired_cache()
    print(f"  Cleaned {cleaned} expired entries")
    
    print(f"\n✅ Production Performance Backend test completed!")