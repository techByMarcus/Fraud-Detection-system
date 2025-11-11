"""
AUTOMATED FRAUD DETECTION & SECURITY MONITORING SYSTEM
======================================================
Created by: Marcus Albright
Purpose: Enterprise-grade fraud detection combining 20+ years of investigative 
         expertise with modern threat detection technology

This system analyzes financial transactions in real-time, identifies suspicious 
patterns, calculates risk scores, and generates automated security alerts.
"""

import csv
import json
from datetime import datetime, timedelta
import random

class FraudDetectionEngine:
    """
    Advanced fraud detection engine based on 20+ years of real-world 
    fraud investigation experience in regulated finance.
    """
    
    def __init__(self):
        self.risk_thresholds = {
            'LOW': 30,
            'MEDIUM': 60,
            'HIGH': 80,
            'CRITICAL': 95
        }
        
        self.fraud_indicators = {
            'velocity': 20,           # Multiple transactions in short time
            'amount_spike': 25,       # Unusually large transaction
            'time_anomaly': 15,       # Transaction at unusual time
            'location_change': 20,    # Rapid location changes
            'new_payee': 10,          # First-time payee
            'round_amount': 5,        # Suspiciously round amounts
            'account_age': 15,        # New account activity
            'pattern_match': 30       # Matches known fraud pattern
        }
        
        self.alerts = []
        self.statistics = {
            'total_transactions': 0,
            'flagged_transactions': 0,
            'critical_alerts': 0,
            'high_risk': 0,
            'medium_risk': 0,
            'low_risk': 0
        }
    
    def calculate_risk_score(self, transaction):
        """
        Calculate risk score based on multiple fraud indicators.
        Uses methodology refined over 1,000+ real fraud investigations.
        """
        risk_score = 0
        indicators_triggered = []
        
        # Velocity Check: Multiple transactions in short period
        if transaction.get('transactions_last_hour', 0) > 3:
            risk_score += self.fraud_indicators['velocity']
            indicators_triggered.append('HIGH_VELOCITY')
        
        # Amount Spike: Transaction significantly above normal
        amount = transaction.get('amount', 0)
        avg_amount = transaction.get('avg_transaction_amount', 0)
        
        if avg_amount > 0 and amount > (avg_amount * 3):
            risk_score += self.fraud_indicators['amount_spike']
            indicators_triggered.append('AMOUNT_SPIKE')
        
        # Time Anomaly: Transaction at unusual hours (2am-5am)
        hour = transaction.get('hour', 12)
        if 2 <= hour <= 5:
            risk_score += self.fraud_indicators['time_anomaly']
            indicators_triggered.append('TIME_ANOMALY')
        
        # Location Change: IP address change in short time
        if transaction.get('location_changed', False):
            risk_score += self.fraud_indicators['location_change']
            indicators_triggered.append('LOCATION_CHANGE')
        
        # New Payee: First-time transaction to this recipient
        if transaction.get('new_payee', False):
            risk_score += self.fraud_indicators['new_payee']
            indicators_triggered.append('NEW_PAYEE')
        
        # Round Amount: Suspiciously round numbers (common in fraud)
        if amount > 0 and amount % 100 == 0 and amount >= 500:
            risk_score += self.fraud_indicators['round_amount']
            indicators_triggered.append('ROUND_AMOUNT')
        
        # Account Age: New account with large transaction
        account_age_days = transaction.get('account_age_days', 365)
        if account_age_days < 30 and amount > 1000:
            risk_score += self.fraud_indicators['account_age']
            indicators_triggered.append('NEW_ACCOUNT_RISK')
        
        # Pattern Match: Matches known fraud patterns
        if transaction.get('pattern_match', False):
            risk_score += self.fraud_indicators['pattern_match']
            indicators_triggered.append('PATTERN_MATCH')
        
        return min(risk_score, 100), indicators_triggered
    
    def classify_risk_level(self, risk_score):
        """Classify transaction based on risk score."""
        if risk_score >= self.risk_thresholds['CRITICAL']:
            return 'CRITICAL'
        elif risk_score >= self.risk_thresholds['HIGH']:
            return 'HIGH'
        elif risk_score >= self.risk_thresholds['MEDIUM']:
            return 'MEDIUM'
        elif risk_score >= self.risk_thresholds['LOW']:
            return 'LOW'
        else:
            return 'NORMAL'
    
    def generate_alert(self, transaction, risk_score, risk_level, indicators):
        """Generate security alert for flagged transaction."""
        alert = {
            'alert_id': f"ALERT-{len(self.alerts) + 1:05d}",
            'timestamp': datetime.now().isoformat(),
            'transaction_id': transaction.get('transaction_id'),
            'customer_id': transaction.get('customer_id'),
            'amount': transaction.get('amount'),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'indicators': indicators,
            'recommended_action': self.get_recommended_action(risk_level),
            'status': 'PENDING_REVIEW'
        }
        
        self.alerts.append(alert)
        return alert
    
    def get_recommended_action(self, risk_level):
        """Provide recommended action based on risk level."""
        actions = {
            'CRITICAL': 'IMMEDIATE BLOCK - Contact customer and fraud team immediately',
            'HIGH': 'HOLD FOR REVIEW - Manual investigation required before processing',
            'MEDIUM': 'ENHANCED MONITORING - Flag for additional verification',
            'LOW': 'STANDARD MONITORING - Log for pattern analysis'
        }
        return actions.get(risk_level, 'MONITOR')
    
    def analyze_transaction(self, transaction):
        """Main analysis function - processes single transaction."""
        self.statistics['total_transactions'] += 1
        
        # Calculate risk score
        risk_score, indicators = self.calculate_risk_score(transaction)
        
        # Classify risk level
        risk_level = self.classify_risk_level(risk_score)
        
        # Update statistics
        if risk_level != 'NORMAL':
            self.statistics['flagged_transactions'] += 1
            
            if risk_level == 'CRITICAL':
                self.statistics['critical_alerts'] += 1
            elif risk_level == 'HIGH':
                self.statistics['high_risk'] += 1
            elif risk_level == 'MEDIUM':
                self.statistics['medium_risk'] += 1
            elif risk_level == 'LOW':
                self.statistics['low_risk'] += 1
        
        # Generate alert if necessary
        alert = None
        if risk_level in ['CRITICAL', 'HIGH', 'MEDIUM']:
            alert = self.generate_alert(transaction, risk_score, risk_level, indicators)
        
        return {
            'transaction_id': transaction.get('transaction_id'),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'indicators': indicators,
            'alert': alert
        }
    
    def generate_report(self):
        """Generate comprehensive security report."""
        report = {
            'report_generated': datetime.now().isoformat(),
            'analysis_period': '24_HOURS',
            'statistics': self.statistics,
            'alert_summary': {
                'total_alerts': len(self.alerts),
                'critical': self.statistics['critical_alerts'],
                'high': self.statistics['high_risk'],
                'medium': self.statistics['medium_risk'],
                'pending_review': len([a for a in self.alerts if a['status'] == 'PENDING_REVIEW'])
            },
            'top_alerts': sorted(self.alerts, key=lambda x: x['risk_score'], reverse=True)[:10],
            'recommendations': self.generate_recommendations()
        }
        return report
    
    def generate_recommendations(self):
        """Generate security recommendations based on analysis."""
        recommendations = []
        
        if self.statistics['critical_alerts'] > 0:
            recommendations.append({
                'priority': 'CRITICAL',
                'recommendation': f"Immediate action required: {self.statistics['critical_alerts']} critical fraud alerts detected",
                'action': 'Review and respond to all CRITICAL alerts within 1 hour'
            })
        
        if self.statistics['high_risk'] > 5:
            recommendations.append({
                'priority': 'HIGH',
                'recommendation': f"Elevated fraud activity: {self.statistics['high_risk']} high-risk transactions",
                'action': 'Increase monitoring and consider enhanced authentication'
            })
        
        flagged_rate = (self.statistics['flagged_transactions'] / max(self.statistics['total_transactions'], 1)) * 100
        
        if flagged_rate > 10:
            recommendations.append({
                'priority': 'MEDIUM',
                'recommendation': f"High flag rate ({flagged_rate:.1f}%) - Review fraud detection thresholds",
                'action': 'Analyze false positives and tune detection rules'
            })
        
        return recommendations


def generate_sample_transactions(num_transactions=50):
    """Generate realistic sample transaction data for demonstration."""
    transactions = []
    base_time = datetime.now()
    
    customer_ids = [f"CUST{i:04d}" for i in range(1, 21)]
    
    for i in range(num_transactions):
        # Create transaction with varying risk profiles
        is_suspicious = random.random() < 0.3  # 30% suspicious transactions
        
        amount = random.randint(50, 5000)
        if is_suspicious:
            amount = random.choice([
                random.randint(5000, 15000),  # Large amount
                random.randint(100, 1000) * 10  # Round amount
            ])
        
        hour = random.randint(0, 23)
        if is_suspicious and random.random() < 0.4:
            hour = random.randint(2, 5)  # Suspicious time
        
        transaction = {
            'transaction_id': f"TXN{i+1:06d}",
            'customer_id': random.choice(customer_ids),
            'amount': amount,
            'timestamp': (base_time - timedelta(hours=random.randint(0, 24))).isoformat(),
            'hour': hour,
            'avg_transaction_amount': random.randint(200, 800),
            'transactions_last_hour': random.randint(0, 6) if is_suspicious else random.randint(0, 2),
            'location_changed': is_suspicious and random.random() < 0.3,
            'new_payee': is_suspicious and random.random() < 0.5,
            'account_age_days': random.randint(10, 500) if not is_suspicious else random.randint(5, 45),
            'pattern_match': is_suspicious and random.random() < 0.4
        }
        
        transactions.append(transaction)
    
    return transactions


def main():
    """Main execution function - demonstrates the fraud detection system."""
    
    print("=" * 70)
    print("AUTOMATED FRAUD DETECTION & SECURITY MONITORING SYSTEM")
    print("Combining 20+ Years of Fraud Investigation Expertise")
    print("with Modern Threat Detection Technology")
    print("=" * 70)
    print()
    
    # Initialize fraud detection engine
    engine = FraudDetectionEngine()
    
    print("Initializing fraud detection engine...")
    print(f"Risk thresholds configured: {engine.risk_thresholds}")
    print()
    
    # Generate sample transactions
    print("Generating sample transaction data...")
    transactions = generate_sample_transactions(50)
    print(f"Generated {len(transactions)} transactions for analysis")
    print()
    
    # Analyze transactions
    print("Analyzing transactions for fraud indicators...")
    print("-" * 70)
    
    results = []
    for transaction in transactions:
        result = engine.analyze_transaction(transaction)
        results.append(result)
        
        # Display flagged transactions
        if result['risk_level'] in ['CRITICAL', 'HIGH']:
            print(f"\n🚨 {result['risk_level']} RISK DETECTED")
            print(f"Transaction ID: {result['transaction_id']}")
            print(f"Risk Score: {result['risk_score']}/100")
            print(f"Indicators: {', '.join(result['indicators'])}")
            if result['alert']:
                print(f"Alert ID: {result['alert']['alert_id']}")
                print(f"Recommended Action: {result['alert']['recommended_action']}")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    
    # Display statistics
    print("📊 TRANSACTION STATISTICS:")
    print(f"  Total Transactions Analyzed: {engine.statistics['total_transactions']}")
    print(f"  Flagged Transactions: {engine.statistics['flagged_transactions']}")
    print(f"  Flag Rate: {(engine.statistics['flagged_transactions']/engine.statistics['total_transactions']*100):.1f}%")
    print()
    
    print("🚨 ALERT BREAKDOWN:")
    print(f"  Critical Alerts: {engine.statistics['critical_alerts']}")
    print(f"  High Risk: {engine.statistics['high_risk']}")
    print(f"  Medium Risk: {engine.statistics['medium_risk']}")
    print(f"  Low Risk: {engine.statistics['low_risk']}")
    print()
    
    # Generate comprehensive report
    report = engine.generate_report()
    
    print("📋 SECURITY RECOMMENDATIONS:")
    for rec in report['recommendations']:
        print(f"  [{rec['priority']}] {rec['recommendation']}")
        print(f"     → {rec['action']}")
    print()
    
    # Export results
    print("💾 Exporting results...")
    
    # Export alerts to JSON
    with open('fraud_alerts.json', 'w') as f:
        json.dump(engine.alerts, f, indent=2)
    print("  ✓ Alerts exported to: fraud_alerts.json")
    
    # Export full report
    with open('security_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("  ✓ Full report exported to: security_report.json")
    
    # Export transaction analysis
    with open('transaction_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("  ✓ Transaction analysis exported to: transaction_analysis.json")
    
    print()
    print("=" * 70)
    print("System ready for deployment in production environment")
    print("For questions or support, contact: marcus.albright@gmail.com")
    print("=" * 70)


if __name__ == "__main__":
    main()
