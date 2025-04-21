"""
Fraud Detection Module for BloxAPI

This module provides fraud detection and prevention capabilities for
in-game transactions, user accounts, and virtual items.
"""

import os
import re
import time
import json
import logging
import hashlib
import threading
from typing import Dict, List, Any, Optional, Union, Callable, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter, deque
import uuid
import math
import ipaddress

# Configure logging
logger = logging.getLogger(__name__)

class FraudDetectionError(Exception):
    """Exception raised for fraud detection issues"""
    pass

class TransactionMonitor:
    """
    Monitor transactions for suspicious patterns
    """
    
    def __init__(self, max_history: int = 10000):
        """
        Initialize transaction monitor
        
        Args:
            max_history: Maximum number of transactions to keep in history
        """
        self.max_history = max_history
        self.transaction_history: deque = deque(maxlen=max_history)
        self.user_transactions: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        self.item_transactions: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        self.suspicious_transactions: List[Dict[str, Any]] = []
        self.block_list: Set[int] = set()  # User IDs to block
        self.whitelist: Set[int] = set()   # User IDs to allow
        self.lock = threading.RLock()
        
        # Thresholds for detection
        self.thresholds = {
            'transaction_velocity': {  # Transactions per user per minute
                'warning': 5,
                'suspicious': 10,
                'block': 20
            },
            'price_ratio': {  # Ratio relative to average price
                'warning': 5,
                'suspicious': 10,
                'block': 20
            },
            'transaction_amount': {  # Raw transaction amount in Robux
                'warning': 10000,
                'suspicious': 50000,
                'block': 100000
            },
            'new_account_transaction': {  # Account age in days for high-value transactions
                'warning': 30,
                'suspicious': 7,
                'block': 1
            }
        }
    
    def record_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record a transaction and check for fraud indicators
        
        Args:
            transaction: Transaction data with at least these keys:
                - id: Transaction ID
                - user_id: User ID
                - item_id: Item ID
                - amount: Transaction amount
                - currency: Currency code
                - timestamp: Transaction timestamp (ISO format)
                
        Returns:
            Dictionary with fraud detection results
        """
        with self.lock:
            # Normalize transaction data
            if 'timestamp' not in transaction:
                transaction['timestamp'] = datetime.now().isoformat()
            
            if 'id' not in transaction:
                transaction['id'] = str(uuid.uuid4())
            
            # Convert timestamp to datetime if it's a string
            if isinstance(transaction['timestamp'], str):
                transaction['timestamp'] = datetime.fromisoformat(transaction['timestamp'])
            
            # Add to history
            self.transaction_history.append(transaction)
            
            # Update user and item transaction history
            user_id = transaction.get('user_id')
            item_id = transaction.get('item_id')
            
            if user_id:
                self.user_transactions[user_id].append(transaction)
                
                # Limit history size per user
                if len(self.user_transactions[user_id]) > 1000:
                    self.user_transactions[user_id] = self.user_transactions[user_id][-1000:]
            
            if item_id:
                self.item_transactions[item_id].append(transaction)
                
                # Limit history size per item
                if len(self.item_transactions[item_id]) > 1000:
                    self.item_transactions[item_id] = self.item_transactions[item_id][-1000:]
            
            # Check for fraud indicators
            return self.check_transaction(transaction)
    
    def check_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a transaction for fraud indicators
        
        Args:
            transaction: Transaction data
                
        Returns:
            Dictionary with fraud detection results
        """
        user_id = transaction.get('user_id')
        item_id = transaction.get('item_id')
        amount = transaction.get('amount', 0)
        currency = transaction.get('currency', 'Robux')
        timestamp = transaction.get('timestamp', datetime.now())
        
        # Initialize result
        result = {
            'transaction_id': transaction.get('id'),
            'user_id': user_id,
            'item_id': item_id,
            'timestamp': timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp,
            'is_suspicious': False,
            'is_blocked': False,
            'risk_score': 0,
            'risk_factors': [],
            'action': 'allow'
        }
        
        # Skip if user is whitelisted
        if user_id in self.whitelist:
            result['action'] = 'allow'
            result['is_whitelisted'] = True
            return result
        
        # Block if user is on block list
        if user_id in self.block_list:
            result['is_blocked'] = True
            result['action'] = 'block'
            result['risk_factors'].append('User on block list')
            result['risk_score'] = 100
            return result
        
        # Calculate risk based on various factors
        risk_score = 0
        
        # 1. Check transaction velocity (how many transactions by this user recently)
        if user_id:
            recent_transactions = [
                t for t in self.user_transactions.get(user_id, [])
                if isinstance(t.get('timestamp'), datetime) and 
                (timestamp - t.get('timestamp')).total_seconds() < 60  # Last minute
            ]
            
            velocity = len(recent_transactions)
            
            thresholds = self.thresholds['transaction_velocity']
            if velocity >= thresholds['block']:
                risk_score += 50
                result['risk_factors'].append(f"Very high transaction velocity: {velocity} per minute")
            elif velocity >= thresholds['suspicious']:
                risk_score += 30
                result['risk_factors'].append(f"High transaction velocity: {velocity} per minute")
            elif velocity >= thresholds['warning']:
                risk_score += 10
                result['risk_factors'].append(f"Elevated transaction velocity: {velocity} per minute")
        
        # 2. Check price anomalies (is the price much different from usual?)
        if item_id:
            item_prices = [
                t.get('amount', 0) for t in self.item_transactions.get(item_id, [])
                if t.get('currency') == currency
            ]
            
            if item_prices:
                avg_price = sum(item_prices) / len(item_prices)
                if avg_price > 0:
                    price_ratio = amount / avg_price
                    
                    thresholds = self.thresholds['price_ratio']
                    if price_ratio >= thresholds['block'] or price_ratio <= 1/thresholds['block']:
                        risk_score += 40
                        result['risk_factors'].append(f"Extreme price anomaly: {price_ratio:.2f}x average")
                    elif price_ratio >= thresholds['suspicious'] or price_ratio <= 1/thresholds['suspicious']:
                        risk_score += 25
                        result['risk_factors'].append(f"Significant price anomaly: {price_ratio:.2f}x average")
                    elif price_ratio >= thresholds['warning'] or price_ratio <= 1/thresholds['warning']:
                        risk_score += 10
                        result['risk_factors'].append(f"Unusual price: {price_ratio:.2f}x average")
        
        # 3. Check high-value transactions
        if amount > 0:
            thresholds = self.thresholds['transaction_amount']
            if amount >= thresholds['block']:
                risk_score += 30
                result['risk_factors'].append(f"Very high value transaction: {amount} {currency}")
            elif amount >= thresholds['suspicious']:
                risk_score += 20
                result['risk_factors'].append(f"High value transaction: {amount} {currency}")
            elif amount >= thresholds['warning']:
                risk_score += 5
                result['risk_factors'].append(f"Notable transaction value: {amount} {currency}")
        
        # 4. Check account age for high-value transactions
        account_age_days = transaction.get('account_age_days')
        if account_age_days is not None and amount > thresholds['transaction_amount']['warning']:
            thresholds = self.thresholds['new_account_transaction']
            if account_age_days <= thresholds['block']:
                risk_score += 40
                result['risk_factors'].append(f"Brand new account ({account_age_days} days) making high-value transaction")
            elif account_age_days <= thresholds['suspicious']:
                risk_score += 25
                result['risk_factors'].append(f"Very new account ({account_age_days} days) making high-value transaction")
            elif account_age_days <= thresholds['warning']:
                risk_score += 10
                result['risk_factors'].append(f"Relatively new account ({account_age_days} days) making high-value transaction")
        
        # Update result with risk score
        result['risk_score'] = min(100, risk_score)
        
        # Determine action based on risk score
        if risk_score >= 70:
            result['is_suspicious'] = True
            result['is_blocked'] = True
            result['action'] = 'block'
            
            # Add to suspicious transactions
            self.suspicious_transactions.append({
                'transaction': transaction,
                'risk_score': risk_score,
                'risk_factors': result['risk_factors'],
                'timestamp': datetime.now().isoformat()
            })
            
        elif risk_score >= 40:
            result['is_suspicious'] = True
            result['action'] = 'review'
            
            # Add to suspicious transactions
            self.suspicious_transactions.append({
                'transaction': transaction,
                'risk_score': risk_score,
                'risk_factors': result['risk_factors'],
                'timestamp': datetime.now().isoformat()
            })
            
        elif risk_score >= 20:
            result['action'] = 'monitor'
        
        return result
    
    def get_suspicious_transactions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent suspicious transactions
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            List of suspicious transactions
        """
        with self.lock:
            # Sort by timestamp (newest first)
            sorted_transactions = sorted(
                self.suspicious_transactions,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )
            
            return sorted_transactions[:limit]
    
    def get_user_risk_score(self, user_id: int) -> Dict[str, Any]:
        """
        Get a risk score for a user based on their transaction history
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with risk assessment
        """
        with self.lock:
            # Get user's transactions
            transactions = self.user_transactions.get(user_id, [])
            
            if not transactions:
                return {
                    'user_id': user_id,
                    'risk_score': 0,
                    'risk_factors': [],
                    'transaction_count': 0,
                    'is_suspicious': False
                }
            
            # Calculate metrics
            transaction_count = len(transactions)
            recent_transactions = [
                t for t in transactions
                if isinstance(t.get('timestamp'), datetime) and 
                (datetime.now() - t.get('timestamp')).total_seconds() < 86400  # Last 24 hours
            ]
            recent_count = len(recent_transactions)
            
            # Calculate transaction velocity
            if recent_count > 0:
                if recent_count >= 100:
                    transaction_velocity = recent_count / 86400 * 60  # Transactions per minute
                else:
                    # More precise calculation for fewer transactions
                    if recent_count > 1:
                        timestamps = sorted([t.get('timestamp') for t in recent_transactions 
                                          if isinstance(t.get('timestamp'), datetime)])
                        if len(timestamps) > 1:
                            time_span = (timestamps[-1] - timestamps[0]).total_seconds()
                            if time_span > 0:
                                transaction_velocity = (len(timestamps) - 1) / time_span * 60
                            else:
                                transaction_velocity = 0
                        else:
                            transaction_velocity = 0
                    else:
                        transaction_velocity = 0
            else:
                transaction_velocity = 0
            
            # Calculate value statistics
            amounts = [t.get('amount', 0) for t in transactions]
            if amounts:
                avg_amount = sum(amounts) / len(amounts)
                max_amount = max(amounts)
                
                # Calculate standard deviation
                if len(amounts) > 1:
                    variance = sum((x - avg_amount) ** 2 for x in amounts) / len(amounts)
                    std_dev = math.sqrt(variance)
                else:
                    std_dev = 0
            else:
                avg_amount = 0
                max_amount = 0
                std_dev = 0
            
            # Initialize risk factors
            risk_factors = []
            risk_score = 0
            
            # Velocity risk
            velocity_thresholds = self.thresholds['transaction_velocity']
            if transaction_velocity >= velocity_thresholds['block']:
                risk_score += 40
                risk_factors.append(f"Very high transaction velocity: {transaction_velocity:.2f} per minute")
            elif transaction_velocity >= velocity_thresholds['suspicious']:
                risk_score += 25
                risk_factors.append(f"High transaction velocity: {transaction_velocity:.2f} per minute")
            elif transaction_velocity >= velocity_thresholds['warning']:
                risk_score += 10
                risk_factors.append(f"Elevated transaction velocity: {transaction_velocity:.2f} per minute")
            
            # High value transaction risk
            amount_thresholds = self.thresholds['transaction_amount']
            if max_amount >= amount_thresholds['block']:
                risk_score += 30
                risk_factors.append(f"Very high value transaction: {max_amount}")
            elif max_amount >= amount_thresholds['suspicious']:
                risk_score += 20
                risk_factors.append(f"High value transaction: {max_amount}")
            elif max_amount >= amount_thresholds['warning']:
                risk_score += 5
                risk_factors.append(f"Notable transaction value: {max_amount}")
            
            # Value volatility risk
            if avg_amount > 0 and std_dev > 0:
                coefficient_of_variation = std_dev / avg_amount
                if coefficient_of_variation > 2:
                    risk_score += 15
                    risk_factors.append(f"High transaction value volatility: {coefficient_of_variation:.2f}x")
                elif coefficient_of_variation > 1:
                    risk_score += 5
                    risk_factors.append(f"Moderate transaction value volatility: {coefficient_of_variation:.2f}x")
            
            # Return risk assessment
            return {
                'user_id': user_id,
                'risk_score': min(100, risk_score),
                'risk_factors': risk_factors,
                'transaction_count': transaction_count,
                'recent_transaction_count': recent_count,
                'transaction_velocity': transaction_velocity,
                'avg_transaction_value': avg_amount,
                'max_transaction_value': max_amount,
                'is_suspicious': risk_score >= 40
            }
    
    def add_to_blocklist(self, user_id: int) -> None:
        """
        Add a user to the blocklist
        
        Args:
            user_id: User ID to block
        """
        with self.lock:
            self.block_list.add(user_id)
            # Remove from whitelist if present
            if user_id in self.whitelist:
                self.whitelist.remove(user_id)
    
    def add_to_whitelist(self, user_id: int) -> None:
        """
        Add a user to the whitelist
        
        Args:
            user_id: User ID to whitelist
        """
        with self.lock:
            self.whitelist.add(user_id)
            # Remove from blocklist if present
            if user_id in self.block_list:
                self.block_list.remove(user_id)
    
    def set_threshold(self, category: str, level: str, value: float) -> bool:
        """
        Set a detection threshold
        
        Args:
            category: Threshold category (e.g., 'transaction_velocity')
            level: Threshold level (warning, suspicious, block)
            value: Threshold value
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            if category in self.thresholds and level in self.thresholds[category]:
                self.thresholds[category][level] = value
                return True
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get transaction monitoring statistics
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            # Count transactions by day
            daily_counts = defaultdict(int)
            for transaction in self.transaction_history:
                timestamp = transaction.get('timestamp')
                if isinstance(timestamp, datetime):
                    day = timestamp.date().isoformat()
                    daily_counts[day] += 1
            
            return {
                'total_transactions': len(self.transaction_history),
                'unique_users': len(self.user_transactions),
                'unique_items': len(self.item_transactions),
                'suspicious_transactions': len(self.suspicious_transactions),
                'blocked_users': len(self.block_list),
                'whitelisted_users': len(self.whitelist),
                'daily_transaction_counts': dict(daily_counts),
                'thresholds': self.thresholds
            }


class AccountMonitor:
    """
    Monitor user accounts for suspicious activities
    """
    
    def __init__(self):
        """Initialize account monitor"""
        self.suspicious_users: Dict[int, Dict[str, Any]] = {}
        self.suspicious_ips: Dict[str, Dict[str, Any]] = {}
        self.user_ip_mapping: Dict[int, Set[str]] = defaultdict(set)
        self.ip_user_mapping: Dict[str, Set[int]] = defaultdict(set)
        self.lock = threading.RLock()
        
        # Thresholds for detection
        self.thresholds = {
            'login_attempts': {  # Failed login attempts
                'warning': 3,
                'suspicious': 5,
                'block': 10
            },
            'account_age': {  # Account age in days for risk scoring
                'high_risk': 1,
                'medium_risk': 7,
                'low_risk': 30
            },
            'devices_per_account': {  # Number of different devices
                'warning': 3,
                'suspicious': 5,
                'block': 10
            },
            'accounts_per_ip': {  # Number of accounts per IP
                'warning': 3,
                'suspicious': 5,
                'block': 10
            },
            'location_changes': {  # Number of distinct locations
                'warning': 3,
                'suspicious': 5,
                'block': 8
            }
        }
    
    def record_login(self, user_id: int, ip: str, success: bool, 
                    user_agent: str = None, location: str = None,
                    device_id: str = None) -> Dict[str, Any]:
        """
        Record a login attempt and check for suspicious indicators
        
        Args:
            user_id: User ID
            ip: IP address
            success: Whether login was successful
            user_agent: User agent string
            location: Geographic location (e.g., "US-NY")
            device_id: Unique device identifier
            
        Returns:
            Dictionary with account monitoring results
        """
        with self.lock:
            # Update user-IP mappings
            self.user_ip_mapping[user_id].add(ip)
            self.ip_user_mapping[ip].add(user_id)
            
            # Create login record
            login_data = {
                'user_id': user_id,
                'ip': ip,
                'success': success,
                'timestamp': datetime.now(),
                'user_agent': user_agent,
                'location': location,
                'device_id': device_id
            }
            
            # Initialize or update user record
            if user_id not in self.suspicious_users:
                self.suspicious_users[user_id] = {
                    'user_id': user_id,
                    'login_attempts': [],
                    'failed_attempts': 0,
                    'suspicious_activity': False,
                    'risk_score': 0,
                    'risk_factors': [],
                    'last_updated': datetime.now(),
                    'locations': set(),
                    'devices': set(),
                    'ips': set()
                }
            
            user_record = self.suspicious_users[user_id]
            user_record['login_attempts'].append(login_data)
            user_record['last_updated'] = datetime.now()
            user_record['ips'].add(ip)
            
            if not success:
                user_record['failed_attempts'] += 1
            
            if location:
                user_record['locations'].add(location)
            
            if device_id:
                user_record['devices'].add(device_id)
            
            # Initialize or update IP record
            if ip not in self.suspicious_ips:
                self.suspicious_ips[ip] = {
                    'ip': ip,
                    'login_attempts': [],
                    'failed_attempts': 0,
                    'suspicious_activity': False,
                    'risk_score': 0,
                    'risk_factors': [],
                    'last_updated': datetime.now(),
                    'unique_users': set()
                }
            
            ip_record = self.suspicious_ips[ip]
            ip_record['login_attempts'].append(login_data)
            ip_record['last_updated'] = datetime.now()
            ip_record['unique_users'].add(user_id)
            
            if not success:
                ip_record['failed_attempts'] += 1
            
            # Limit login history size
            if len(user_record['login_attempts']) > 100:
                user_record['login_attempts'] = user_record['login_attempts'][-100:]
            
            if len(ip_record['login_attempts']) > 100:
                ip_record['login_attempts'] = ip_record['login_attempts'][-100:]
            
            # Update risk scores
            self._update_user_risk(user_id)
            self._update_ip_risk(ip)
            
            # Get combined risk assessment
            return self._get_login_risk_assessment(user_id, ip, success)
    
    def _update_user_risk(self, user_id: int) -> None:
        """
        Update risk score for a user
        
        Args:
            user_id: User ID to update
        """
        if user_id not in self.suspicious_users:
            return
        
        user_record = self.suspicious_users[user_id]
        risk_factors = []
        risk_score = 0
        
        # 1. Check failed login attempts
        failed_attempts = user_record['failed_attempts']
        thresholds = self.thresholds['login_attempts']
        
        if failed_attempts >= thresholds['block']:
            risk_score += 40
            risk_factors.append(f"Multiple failed login attempts: {failed_attempts}")
        elif failed_attempts >= thresholds['suspicious']:
            risk_score += 25
            risk_factors.append(f"Several failed login attempts: {failed_attempts}")
        elif failed_attempts >= thresholds['warning']:
            risk_score += 10
            risk_factors.append(f"Some failed login attempts: {failed_attempts}")
        
        # 2. Check number of distinct devices
        devices_count = len(user_record['devices'])
        thresholds = self.thresholds['devices_per_account']
        
        if devices_count >= thresholds['block']:
            risk_score += 30
            risk_factors.append(f"Unusually high number of devices: {devices_count}")
        elif devices_count >= thresholds['suspicious']:
            risk_score += 20
            risk_factors.append(f"Many different devices: {devices_count}")
        elif devices_count >= thresholds['warning']:
            risk_score += 5
            risk_factors.append(f"Multiple devices: {devices_count}")
        
        # 3. Check number of distinct locations
        locations_count = len(user_record['locations'])
        thresholds = self.thresholds['location_changes']
        
        if locations_count >= thresholds['block']:
            risk_score += 35
            risk_factors.append(f"Extremely unusual location pattern: {locations_count} distinct locations")
        elif locations_count >= thresholds['suspicious']:
            risk_score += 25
            risk_factors.append(f"Suspicious location pattern: {locations_count} distinct locations")
        elif locations_count >= thresholds['warning']:
            risk_score += 10
            risk_factors.append(f"Multiple locations: {locations_count} distinct locations")
        
        # 4. Check for rapid location changes
        if len(user_record['login_attempts']) >= 2:
            location_login_attempts = [
                a for a in user_record['login_attempts'] 
                if a.get('location') and a.get('success')
            ]
            
            if len(location_login_attempts) >= 2:
                # Sort by timestamp
                sorted_attempts = sorted(
                    location_login_attempts,
                    key=lambda x: x.get('timestamp', datetime.min)
                )
                
                for i in range(1, len(sorted_attempts)):
                    prev_attempt = sorted_attempts[i-1]
                    curr_attempt = sorted_attempts[i]
                    
                    # If locations differ and time difference is small
                    if (prev_attempt.get('location') != curr_attempt.get('location') and
                        isinstance(prev_attempt.get('timestamp'), datetime) and
                        isinstance(curr_attempt.get('timestamp'), datetime)):
                        
                        time_diff = (curr_attempt['timestamp'] - prev_attempt['timestamp']).total_seconds() / 3600  # hours
                        
                        # Check for impossible travel
                        if time_diff < 2:  # Less than 2 hours between logins from different locations
                            risk_score += 50
                            risk_factors.append(
                                f"Impossible travel: {prev_attempt['location']} to {curr_attempt['location']} "
                                f"in {time_diff:.1f} hours"
                            )
                            break
                        elif time_diff < 6:  # Less than 6 hours
                            risk_score += 30
                            risk_factors.append(
                                f"Suspicious travel time: {prev_attempt['location']} to {curr_attempt['location']} "
                                f"in {time_diff:.1f} hours"
                            )
                            break
        
        # Update risk data
        user_record['risk_score'] = min(100, risk_score)
        user_record['risk_factors'] = risk_factors
        user_record['suspicious_activity'] = risk_score >= 40
    
    def _update_ip_risk(self, ip: str) -> None:
        """
        Update risk score for an IP address
        
        Args:
            ip: IP address to update
        """
        if ip not in self.suspicious_ips:
            return
        
        ip_record = self.suspicious_ips[ip]
        risk_factors = []
        risk_score = 0
        
        # 1. Check failed login attempts
        failed_attempts = ip_record['failed_attempts']
        thresholds = self.thresholds['login_attempts']
        
        if failed_attempts >= thresholds['block']:
            risk_score += 40
            risk_factors.append(f"Multiple failed login attempts: {failed_attempts}")
        elif failed_attempts >= thresholds['suspicious']:
            risk_score += 25
            risk_factors.append(f"Several failed login attempts: {failed_attempts}")
        elif failed_attempts >= thresholds['warning']:
            risk_score += 10
            risk_factors.append(f"Some failed login attempts: {failed_attempts}")
        
        # 2. Check number of unique users
        users_count = len(ip_record['unique_users'])
        thresholds = self.thresholds['accounts_per_ip']
        
        if users_count >= thresholds['block']:
            risk_score += 40
            risk_factors.append(f"Extremely high number of accounts: {users_count}")
        elif users_count >= thresholds['suspicious']:
            risk_score += 25
            risk_factors.append(f"Unusually high number of accounts: {users_count}")
        elif users_count >= thresholds['warning']:
            risk_score += 10
            risk_factors.append(f"Multiple accounts: {users_count}")
        
        # 3. Check login velocity
        recent_attempts = [
            a for a in ip_record['login_attempts']
            if isinstance(a.get('timestamp'), datetime) and 
            (datetime.now() - a.get('timestamp')).total_seconds() < 3600  # Last hour
        ]
        
        attempts_count = len(recent_attempts)
        if attempts_count >= 30:  # More than 30 login attempts in an hour
            risk_score += 30
            risk_factors.append(f"Extremely high login frequency: {attempts_count} in the last hour")
        elif attempts_count >= 15:  # More than 15 login attempts in an hour
            risk_score += 20
            risk_factors.append(f"High login frequency: {attempts_count} in the last hour")
        elif attempts_count >= 7:  # More than 7 login attempts in an hour
            risk_score += 5
            risk_factors.append(f"Elevated login frequency: {attempts_count} in the last hour")
        
        # 4. Check if IP is a known proxy or VPN
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check if IP is in a suspicious range
            suspicious_ranges = [
                # Some known proxy/VPN networks - simplified for example
                ipaddress.ip_network('185.220.101.0/24'),  # Tor exit nodes
                ipaddress.ip_network('104.244.72.0/21'),   # Twitter/X known proxy
                ipaddress.ip_network('163.172.0.0/16'),    # OVH/SYS
            ]
            
            for network in suspicious_ranges:
                if ip_obj in network:
                    risk_score += 15
                    risk_factors.append(f"IP from known proxy/VPN range: {network}")
                    break
        except ValueError:
            pass  # Invalid IP format
        
        # Update risk data
        ip_record['risk_score'] = min(100, risk_score)
        ip_record['risk_factors'] = risk_factors
        ip_record['suspicious_activity'] = risk_score >= 40
    
    def _get_login_risk_assessment(self, user_id: int, ip: str, success: bool) -> Dict[str, Any]:
        """
        Get combined risk assessment for a login attempt
        
        Args:
            user_id: User ID
            ip: IP address
            success: Whether login was successful
            
        Returns:
            Dictionary with risk assessment
        """
        user_record = self.suspicious_users.get(user_id, {})
        ip_record = self.suspicious_ips.get(ip, {})
        
        user_risk = user_record.get('risk_score', 0)
        ip_risk = ip_record.get('risk_score', 0)
        
        # Combine risk scores, giving more weight to the higher risk
        combined_risk = max(user_risk, ip_risk) * 0.7 + min(user_risk, ip_risk) * 0.3
        
        # Get combined risk factors
        risk_factors = []
        risk_factors.extend(user_record.get('risk_factors', []))
        risk_factors.extend(ip_record.get('risk_factors', []))
        
        # Determine if login should be blocked
        should_block = combined_risk >= 70 or user_risk >= 70 or ip_risk >= 70
        
        # Failed login but not blocked should be monitored
        if not success and not should_block:
            action = 'monitor'
        elif should_block:
            action = 'block'
        elif combined_risk >= 40:
            action = 'review'
        else:
            action = 'allow'
        
        return {
            'user_id': user_id,
            'ip': ip,
            'success': success,
            'user_risk_score': user_risk,
            'ip_risk_score': ip_risk,
            'combined_risk_score': combined_risk,
            'risk_factors': risk_factors,
            'is_suspicious': combined_risk >= 40,
            'is_blocked': should_block,
            'action': action,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_suspicious_users(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get suspicious users
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List of suspicious user records
        """
        with self.lock:
            # Sort by risk score (highest first)
            sorted_users = sorted(
                [u for u in self.suspicious_users.values() if u.get('suspicious_activity', False)],
                key=lambda x: x.get('risk_score', 0),
                reverse=True
            )
            
            # Convert to serializable format
            result = []
            for user in sorted_users[:limit]:
                user_copy = user.copy()
                user_copy['locations'] = list(user.get('locations', set()))
                user_copy['devices'] = list(user.get('devices', set()))
                user_copy['ips'] = list(user.get('ips', set()))
                
                # Remove login attempts for brevity
                user_copy.pop('login_attempts', None)
                
                # Convert last_updated to string
                if isinstance(user_copy.get('last_updated'), datetime):
                    user_copy['last_updated'] = user_copy['last_updated'].isoformat()
                
                result.append(user_copy)
            
            return result
    
    def get_suspicious_ips(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get suspicious IP addresses
        
        Args:
            limit: Maximum number of IPs to return
            
        Returns:
            List of suspicious IP records
        """
        with self.lock:
            # Sort by risk score (highest first)
            sorted_ips = sorted(
                [ip for ip in self.suspicious_ips.values() if ip.get('suspicious_activity', False)],
                key=lambda x: x.get('risk_score', 0),
                reverse=True
            )
            
            # Convert to serializable format
            result = []
            for ip in sorted_ips[:limit]:
                ip_copy = ip.copy()
                ip_copy['unique_users'] = list(ip.get('unique_users', set()))
                
                # Remove login attempts for brevity
                ip_copy.pop('login_attempts', None)
                
                # Convert last_updated to string
                if isinstance(ip_copy.get('last_updated'), datetime):
                    ip_copy['last_updated'] = ip_copy['last_updated'].isoformat()
                
                result.append(ip_copy)
            
            return result
    
    def get_user_accounts_by_ip(self, ip: str) -> List[int]:
        """
        Get user accounts associated with an IP address
        
        Args:
            ip: IP address
            
        Returns:
            List of user IDs
        """
        with self.lock:
            return list(self.ip_user_mapping.get(ip, set()))
    
    def get_ip_addresses_by_user(self, user_id: int) -> List[str]:
        """
        Get IP addresses associated with a user account
        
        Args:
            user_id: User ID
            
        Returns:
            List of IP addresses
        """
        with self.lock:
            return list(self.user_ip_mapping.get(user_id, set()))
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get account monitoring statistics
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            # Count suspicious users and IPs
            suspicious_users_count = sum(
                1 for u in self.suspicious_users.values() 
                if u.get('suspicious_activity', False)
            )
            
            suspicious_ips_count = sum(
                1 for ip in self.suspicious_ips.values() 
                if ip.get('suspicious_activity', False)
            )
            
            return {
                'total_users': len(self.suspicious_users),
                'total_ips': len(self.suspicious_ips),
                'suspicious_users': suspicious_users_count,
                'suspicious_ips': suspicious_ips_count,
                'total_user_ip_mappings': sum(len(ips) for ips in self.user_ip_mapping.values()),
                'thresholds': self.thresholds
            }


class ItemMonitor:
    """
    Monitor virtual items for suspicious activities
    """
    
    def __init__(self):
        """Initialize item monitor"""
        self.item_data: Dict[int, Dict[str, Any]] = {}
        self.user_items: Dict[int, Set[int]] = defaultdict(set)
        self.suspicious_items: Dict[int, Dict[str, Any]] = {}
        self.lock = threading.RLock()
    
    def record_item_activity(self, item_id: int, event_type: str, 
                           user_id: Optional[int] = None,
                           data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Record an item-related activity
        
        Args:
            item_id: Item ID
            event_type: Event type (e.g., 'create', 'purchase', 'transfer', 'modify')
            user_id: User ID associated with the event
            data: Additional event data
            
        Returns:
            Dictionary with item monitoring results
        """
        with self.lock:
            # Initialize data dictionary
            if data is None:
                data = {}
            
            # Create event record
            event = {
                'item_id': item_id,
                'event_type': event_type,
                'user_id': user_id,
                'timestamp': datetime.now(),
                'data': data
            }
            
            # Initialize or update item record
            if item_id not in self.item_data:
                self.item_data[item_id] = {
                    'item_id': item_id,
                    'events': [],
                    'owners': set(),
                    'creators': set(),
                    'creation_time': None,
                    'last_updated': datetime.now(),
                    'price_history': [],
                    'suspicious_activity': False,
                    'risk_score': 0,
                    'risk_factors': []
                }
            
            item_record = self.item_data[item_id]
            item_record['events'].append(event)
            item_record['last_updated'] = datetime.now()
            
            # Update ownership and creation data
            if event_type == 'create' and user_id is not None:
                item_record['creators'].add(user_id)
                item_record['creation_time'] = datetime.now()
            
            if event_type == 'purchase' and user_id is not None:
                item_record['owners'].add(user_id)
                self.user_items[user_id].add(item_id)
                
                # Record price in history if available
                price = data.get('price')
                if price is not None:
                    item_record['price_history'].append({
                        'price': price,
                        'timestamp': datetime.now(),
                        'currency': data.get('currency', 'Robux')
                    })
            
            # Limit event history size
            if len(item_record['events']) > 100:
                item_record['events'] = item_record['events'][-100:]
            
            # Check for suspicious activity
            self._check_item_suspicious_activity(item_id)
            
            # Return assessment
            return self._get_item_risk_assessment(item_id)
    
    def _check_item_suspicious_activity(self, item_id: int) -> None:
        """
        Check an item for suspicious activity
        
        Args:
            item_id: Item ID to check
        """
        if item_id not in self.item_data:
            return
        
        item_record = self.item_data[item_id]
        risk_factors = []
        risk_score = 0
        
        # 1. Check price volatility
        price_history = item_record.get('price_history', [])
        if len(price_history) >= 2:
            # Sort by timestamp
            sorted_prices = sorted(
                price_history,
                key=lambda x: x.get('timestamp', datetime.min)
            )
            
            # Calculate price changes
            price_changes = []
            for i in range(1, len(sorted_prices)):
                prev_price = sorted_prices[i-1].get('price', 0)
                curr_price = sorted_prices[i].get('price', 0)
                
                if prev_price > 0:
                    price_change = (curr_price - prev_price) / prev_price  # Percentage change
                    price_changes.append(price_change)
            
            if price_changes:
                # Check for extreme price volatility
                max_change = max(abs(change) for change in price_changes)
                
                if max_change > 10:  # 1000% change
                    risk_score += 50
                    risk_factors.append(f"Extreme price volatility: {max_change * 100:.1f}% change")
                elif max_change > 5:  # 500% change
                    risk_score += 30
                    risk_factors.append(f"High price volatility: {max_change * 100:.1f}% change")
                elif max_change > 2:  # 200% change
                    risk_score += 15
                    risk_factors.append(f"Significant price volatility: {max_change * 100:.1f}% change")
                elif max_change > 1:  # 100% change
                    risk_score += 5
                    risk_factors.append(f"Notable price volatility: {max_change * 100:.1f}% change")
        
        # 2. Check for rapid ownership changes
        ownership_events = [
            e for e in item_record.get('events', [])
            if e.get('event_type') in ('purchase', 'transfer')
        ]
        
        if len(ownership_events) >= 3:
            # Sort by timestamp
            sorted_events = sorted(
                ownership_events,
                key=lambda x: x.get('timestamp', datetime.min)
            )
            
            # Check time between ownership changes
            time_between_changes = []
            for i in range(1, len(sorted_events)):
                prev_time = sorted_events[i-1].get('timestamp', datetime.min)
                curr_time = sorted_events[i].get('timestamp', datetime.min)
                
                if isinstance(prev_time, datetime) and isinstance(curr_time, datetime):
                    time_diff = (curr_time - prev_time).total_seconds() / 3600  # hours
                    time_between_changes.append(time_diff)
            
            if time_between_changes:
                min_time = min(time_between_changes)
                
                if min_time < 0.1:  # Less than 6 minutes
                    risk_score += 40
                    risk_factors.append(f"Extremely rapid ownership changes: {min_time:.2f} hours apart")
                elif min_time < 1:  # Less than 1 hour
                    risk_score += 25
                    risk_factors.append(f"Very rapid ownership changes: {min_time:.2f} hours apart")
                elif min_time < 6:  # Less than 6 hours
                    risk_score += 10
                    risk_factors.append(f"Rapid ownership changes: {min_time:.2f} hours apart")
        
        # 3. Check for cyclic trading patterns (money laundering)
        if len(ownership_events) >= 4:
            # Extract sequence of owners
            owner_sequence = []
            for event in sorted(ownership_events, key=lambda x: x.get('timestamp', datetime.min)):
                user_id = event.get('user_id')
                if user_id is not None:
                    owner_sequence.append(user_id)
            
            # Check for repetitions in the sequence
            if len(owner_sequence) >= 4:
                owner_counts = Counter(owner_sequence)
                repeated_owners = [owner for owner, count in owner_counts.items() if count >= 2]
                
                if repeated_owners:
                    # Check for ownership cycles
                    for i in range(len(owner_sequence) - 3):
                        if owner_sequence[i] in owner_sequence[i+2:]:
                            cycle_length = owner_sequence[i+2:].index(owner_sequence[i]) + 2
                            
                            risk_score += 40
                            risk_factors.append(f"Cyclic trading pattern detected (cycle length: {cycle_length})")
                            break
        
        # 4. Check for unusual creation/modification patterns
        creation_time = item_record.get('creation_time')
        modification_events = [
            e for e in item_record.get('events', [])
            if e.get('event_type') == 'modify'
        ]
        
        if creation_time and modification_events:
            # Get first modification after creation
            sorted_mods = sorted(
                modification_events,
                key=lambda x: x.get('timestamp', datetime.min)
            )
            
            first_mod = sorted_mods[0].get('timestamp')
            
            if isinstance(first_mod, datetime) and isinstance(creation_time, datetime):
                mod_delay = (first_mod - creation_time).total_seconds() / 60  # minutes
                
                if mod_delay < 1:  # Less than 1 minute
                    risk_score += 15
                    risk_factors.append(f"Immediate modification after creation: {mod_delay:.1f} minutes")
                elif mod_delay < 5:  # Less than 5 minutes
                    risk_score += 5
                    risk_factors.append(f"Quick modification after creation: {mod_delay:.1f} minutes")
        
        # Update risk data
        item_record['risk_score'] = min(100, risk_score)
        item_record['risk_factors'] = risk_factors
        
        # Detect suspicious activity
        if risk_score >= 40:
            item_record['suspicious_activity'] = True
            
            # Add to suspicious items
            self.suspicious_items[item_id] = item_record.copy()
            
            # Remove events to save space
            self.suspicious_items[item_id].pop('events', None)
        elif item_id in self.suspicious_items:
            # Remove from suspicious items if no longer suspicious
            del self.suspicious_items[item_id]
    
    def _get_item_risk_assessment(self, item_id: int) -> Dict[str, Any]:
        """
        Get risk assessment for an item
        
        Args:
            item_id: Item ID
            
        Returns:
            Dictionary with risk assessment
        """
        if item_id not in self.item_data:
            return {
                'item_id': item_id,
                'risk_score': 0,
                'risk_factors': [],
                'is_suspicious': False,
                'action': 'allow'
            }
        
        item_record = self.item_data[item_id]
        risk_score = item_record.get('risk_score', 0)
        risk_factors = item_record.get('risk_factors', [])
        
        # Determine action based on risk score
        if risk_score >= 70:
            action = 'block'
        elif risk_score >= 40:
            action = 'review'
        elif risk_score >= 20:
            action = 'monitor'
        else:
            action = 'allow'
        
        # Return assessment
        return {
            'item_id': item_id,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'is_suspicious': risk_score >= 40,
            'action': action,
            'owners_count': len(item_record.get('owners', set())),
            'creation_time': item_record.get('creation_time').isoformat() 
                           if isinstance(item_record.get('creation_time'), datetime) else None,
            'last_updated': item_record.get('last_updated').isoformat()
                          if isinstance(item_record.get('last_updated'), datetime) else None
        }
    
    def get_suspicious_items(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get suspicious items
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of suspicious item records
        """
        with self.lock:
            # Sort by risk score (highest first)
            sorted_items = sorted(
                list(self.suspicious_items.values()),
                key=lambda x: x.get('risk_score', 0),
                reverse=True
            )
            
            # Convert to serializable format
            result = []
            for item in sorted_items[:limit]:
                item_copy = item.copy()
                
                # Convert sets to lists
                item_copy['owners'] = list(item.get('owners', set()))
                item_copy['creators'] = list(item.get('creators', set()))
                
                # Convert timestamps to strings
                if isinstance(item_copy.get('creation_time'), datetime):
                    item_copy['creation_time'] = item_copy['creation_time'].isoformat()
                
                if isinstance(item_copy.get('last_updated'), datetime):
                    item_copy['last_updated'] = item_copy['last_updated'].isoformat()
                
                result.append(item_copy)
            
            return result
    
    def get_user_items(self, user_id: int) -> List[int]:
        """
        Get items owned by a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of item IDs
        """
        with self.lock:
            return list(self.user_items.get(user_id, set()))
    
    def get_item_owners(self, item_id: int) -> List[int]:
        """
        Get owners of an item
        
        Args:
            item_id: Item ID
            
        Returns:
            List of user IDs
        """
        with self.lock:
            item_record = self.item_data.get(item_id, {})
            return list(item_record.get('owners', set()))
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get item monitoring statistics
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            # Get total events count
            total_events = sum(
                len(item.get('events', [])) for item in self.item_data.values()
            )
            
            return {
                'total_items': len(self.item_data),
                'suspicious_items': len(self.suspicious_items),
                'total_events': total_events,
                'unique_owners': len(self.user_items)
            }


# Global instances
_transaction_monitor = None
_account_monitor = None
_item_monitor = None

def get_transaction_monitor() -> TransactionMonitor:
    """
    Get the global transaction monitor instance
    
    Returns:
        TransactionMonitor instance
    """
    global _transaction_monitor
    
    if _transaction_monitor is None:
        _transaction_monitor = TransactionMonitor()
    
    return _transaction_monitor

def get_account_monitor() -> AccountMonitor:
    """
    Get the global account monitor instance
    
    Returns:
        AccountMonitor instance
    """
    global _account_monitor
    
    if _account_monitor is None:
        _account_monitor = AccountMonitor()
    
    return _account_monitor

def get_item_monitor() -> ItemMonitor:
    """
    Get the global item monitor instance
    
    Returns:
        ItemMonitor instance
    """
    global _item_monitor
    
    if _item_monitor is None:
        _item_monitor = ItemMonitor()
    
    return _item_monitor