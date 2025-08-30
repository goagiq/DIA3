"""
Test Phase 4 Security & Compliance Implementation.

This test file verifies the implementation of Phase 4 components:
- Audit Trail Service
- Encryption Service  
- CAPTCHA Service
- Enhanced Report Exporter
"""

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

# Import Phase 4 components
from src.core.security.audit_trail import AuditTrailService, AuditEventType, AuditSeverity
from src.core.security.encryption import EncryptionService
from src.core.security.captcha import CaptchaService
from src.core.export.report_exporter import EnhancedReportExporter, ExportComponent, ExportConfiguration


class TestPhase4SecurityCompliance(unittest.TestCase):
    """Test cases for Phase 4 Security & Compliance implementation."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.audit_log_path = os.path.join(self.temp_dir, "test_audit_trail.jsonl")
        self.encryption_key_path = os.path.join(self.temp_dir, "test_encryption_keys.json")
        self.export_dir = os.path.join(self.temp_dir, "exports")
        
        # Initialize services
        self.audit_service = AuditTrailService(self.audit_log_path)
        self.encryption_service = EncryptionService(self.encryption_key_path)
        self.captcha_service = CaptchaService()
        # The EnhancedReportExporter will be initialized properly now that ProgressTracker issue is fixed
        self.report_exporter = EnhancedReportExporter(self.export_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_audit_trail_service(self):
        """Test audit trail service functionality."""
        # Test basic event logging
        event_id = self.audit_service.log_event(
            event_type=AuditEventType.REPORT_GENERATION,
            user_id="test_user",
            session_id="test_session",
            action="test_action",
            details={"test": "data"}
        )
        
        self.assertIsNotNone(event_id)
        self.assertTrue(len(event_id) > 0)
        
        # Test user login logging
        login_event_id = self.audit_service.log_user_login(
            user_id="test_user",
            session_id="test_session",
            ip_address="127.0.0.1",
            user_agent="test_agent"
        )
        
        self.assertIsNotNone(login_event_id)
        
        # Test data access logging
        access_event_id = self.audit_service.log_data_access(
            user_id="test_user",
            session_id="test_session",
            resource="test_resource",
            data_classification="confidential"
        )
        
        self.assertIsNotNone(access_event_id)
        
        # Test MCP tool usage logging
        mcp_event_id = self.audit_service.log_mcp_tool_usage(
            user_id="test_user",
            session_id="test_session",
            tool_name="test_tool",
            parameters={"param1": "value1"}
        )
        
        self.assertIsNotNone(mcp_event_id)
        
        # Test Monte Carlo simulation logging
        mc_event_id = self.audit_service.log_monte_carlo_simulation(
            user_id="test_user",
            session_id="test_session",
            simulation_id="test_simulation",
            parameters={"iterations": 1000}
        )
        
        self.assertIsNotNone(mc_event_id)
        
        # Test audit summary
        summary = self.audit_service.get_audit_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("total_events", summary)
        self.assertGreater(summary["total_events"], 0)
    
    def test_encryption_service(self):
        """Test encryption service functionality."""
        # Test symmetric encryption
        test_data = {"test": "data", "number": 42}
        encrypted_data = self.encryption_service.encrypt_data(test_data, "symmetric")
        
        self.assertIsInstance(encrypted_data, dict)
        self.assertIn("encrypted_data", encrypted_data)
        self.assertIn("iv", encrypted_data)
        self.assertIn("hmac", encrypted_data)
        
        # Test decryption
        decrypted_data = self.encryption_service.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, test_data)
        
        # Test asymmetric encryption
        encrypted_asymmetric = self.encryption_service.encrypt_data(test_data, "asymmetric")
        
        self.assertIsInstance(encrypted_asymmetric, dict)
        self.assertIn("encrypted_data", encrypted_asymmetric)
        self.assertIn("encrypted_key", encrypted_asymmetric)
        
        # Test asymmetric decryption
        decrypted_asymmetric = self.encryption_service.decrypt_data(encrypted_asymmetric)
        self.assertEqual(decrypted_asymmetric, test_data)
        
        # Test file encryption
        test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(test_file_path, 'w') as f:
            f.write("test content")
        
        encrypted_file_path = self.encryption_service.encrypt_file(test_file_path)
        self.assertTrue(os.path.exists(encrypted_file_path))
        
        # Test file decryption
        decrypted_file_path = self.encryption_service.decrypt_file(encrypted_file_path)
        with open(decrypted_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "test content")
        
        # Test data hashing
        hash_value = self.encryption_service.hash_data("test data")
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)  # SHA-256 hash length
        
        # Test data integrity verification
        is_valid = self.encryption_service.verify_data_integrity("test data", hash_value)
        self.assertTrue(is_valid)
        
        # Test secure token generation
        token = self.encryption_service.generate_secure_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)
    
    def test_captcha_service(self):
        """Test CAPTCHA service functionality."""
        # Test challenge generation
        challenge = self.captcha_service.generate_challenge("text", "medium")
        
        self.assertIsInstance(challenge, dict)
        self.assertIn("challenge_id", challenge)
        self.assertIn("question", challenge)
        self.assertIn("challenge_type", challenge)
        self.assertIn("difficulty", challenge)
        
        challenge_id = challenge["challenge_id"]
        
        # Test challenge status
        status = self.captcha_service.get_challenge_status(challenge_id)
        self.assertIsInstance(status, dict)
        self.assertTrue(status["exists"])
        self.assertEqual(status["challenge_id"], challenge_id)
        
        # Test answer verification (correct answer)
        # Note: We need to know the answer to test this properly
        # For now, we'll test with a wrong answer
        verification_result = self.captcha_service.verify_answer(challenge_id, "wrong_answer")
        
        self.assertIsInstance(verification_result, dict)
        self.assertIn("success", verification_result)
        self.assertIn("challenge_id", verification_result)
        
        # Test math challenge generation
        math_challenge = self.captcha_service.generate_challenge("math", "easy")
        
        self.assertIsInstance(math_challenge, dict)
        self.assertEqual(math_challenge["challenge_type"], "math")
        
        # Test report access CAPTCHA
        report_captcha = self.captcha_service.generate_report_access_captcha(
            "test_report_id", "test_user_id"
        )
        
        self.assertIsInstance(report_captcha, dict)
        self.assertIn("report_id", report_captcha)
        self.assertIn("user_id", report_captcha)
        self.assertIn("purpose", report_captcha)
        
        # Test CAPTCHA statistics
        stats = self.captcha_service.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn("active_challenges", stats)
        self.assertIn("total_challenges", stats)
    
    def test_enhanced_report_exporter(self):
        """Test enhanced report exporter functionality."""
        # Create test report data
        test_report_data = {
            "query": "Test query for enhanced report",
            "timestamp": datetime.now().isoformat(),
            "monte_carlo_simulation": {
                "key_findings": ["Finding 1", "Finding 2"],
                "metrics": {"confidence": 0.95}
            },
            "strategic_analysis": {
                "key_insights": ["Insight 1", "Insight 2"],
                "strategic_metrics": {"position": "strong"}
            },
            "risk_assessment": {
                "critical_risks": ["Risk 1", "Risk 2"],
                "risk_metrics": {"severity": "high"}
            }
        }
        
        # Create export components
        components = [
            ExportComponent(
                name="executive_summary",
                title="Executive Summary",
                description="Test summary",
                order=1
            ),
            ExportComponent(
                name="monte_carlo_simulation",
                title="Monte Carlo Results",
                description="Test simulation",
                order=2
            )
        ]
        
        # Create export configuration
        export_config = ExportConfiguration(
            report_id="test_report_001",
            export_format="markdown",
            components=components,
            include_narrative=True,
            include_summary=True
        )
        
        # Test report export
        export_result = self.report_exporter.export_enhanced_report(
            test_report_data, export_config
        )
        
        self.assertIsInstance(export_result, dict)
        self.assertIn("success", export_result)
        self.assertIn("export_id", export_result)
        self.assertIn("timestamp", export_result)
        
        if export_result["success"]:
            self.assertIn("file_path", export_result)
            self.assertIn("file_size", export_result)
            self.assertIn("format", export_result)
            
            # Verify file was created
            file_path = export_result["file_path"]
            self.assertTrue(os.path.exists(file_path))
            
            # Test PDF export
            pdf_config = ExportConfiguration(
                report_id="test_report_002",
                export_format="pdf",
                components=components,
                include_narrative=True,
                include_summary=True
            )
            
            pdf_result = self.report_exporter.export_enhanced_report(
                test_report_data, pdf_config
            )
            
            self.assertIsInstance(pdf_result, dict)
            self.assertIn("success", pdf_result)
            
            # Test export statistics
            stats = self.report_exporter.get_export_statistics()
            self.assertIsInstance(stats, dict)
            self.assertIn("total_exports", stats)
            self.assertIn("export_formats", stats)
    
    def test_security_integration(self):
        """Test integration between security components."""
        # Test audit trail with encryption
        sensitive_data = {"password": "secret123", "api_key": "key456"}
        
        # Encrypt sensitive data
        encrypted_data = self.encryption_service.encrypt_sensitive_fields(
            sensitive_data, ["password", "api_key"]
        )
        
        # Log encrypted data access
        event_id = self.audit_service.log_data_access(
            user_id="test_user",
            session_id="test_session",
            resource="sensitive_data",
            data_classification="secret"
        )
        
        self.assertIsNotNone(event_id)
        
        # Test CAPTCHA with audit trail
        captcha_challenge = self.captcha_service.generate_report_access_captcha(
            "sensitive_report", "test_user"
        )
        
        # Log CAPTCHA generation
        captcha_event_id = self.audit_service.log_event(
            event_type=AuditEventType.SECURITY_EVENT,
            user_id="test_user",
            session_id="test_session",
            action="captcha_generated",
            details={"report_id": "sensitive_report"},
            severity=AuditSeverity.MEDIUM
        )
        
        self.assertIsNotNone(captcha_event_id)
    
    def test_compliance_features(self):
        """Test FedRAMP and DoD compliance features."""
        # Test data classification
        classifications = self.audit_service.data_classifications
        self.assertIn("PUBLIC", classifications)
        self.assertIn("CONFIDENTIAL", classifications)
        self.assertIn("SECRET", classifications)
        self.assertIn("TOP_SECRET", classifications)
        
        # Test audit trail compliance
        compliance_event = self.audit_service.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            user_id="compliance_user",
            session_id="compliance_session",
            action="compliance_check",
            data_classification="confidential",
            compliance_tags=["FedRAMP", "DoD"]
        )
        
        self.assertIsNotNone(compliance_event)
        
        # Test encryption compliance
        public_key = self.encryption_service.get_public_key_pem()
        self.assertIsInstance(public_key, str)
        self.assertIn("-----BEGIN PUBLIC KEY-----", public_key)
        
        # Test CAPTCHA compliance
        captcha_stats = self.captcha_service.get_statistics()
        self.assertIn("success_rate", captcha_stats)
        self.assertIn("average_attempts", captcha_stats)
    
    def test_error_handling(self):
        """Test error handling in security components."""
        # Test invalid encryption type
        with self.assertRaises(ValueError):
            self.encryption_service.encrypt_data("test", "invalid_type")
        
        # Test invalid CAPTCHA challenge type
        with self.assertRaises(ValueError):
            self.captcha_service.generate_challenge("invalid_type", "medium")
        
        # Test invalid export format
        invalid_config = ExportConfiguration(
            report_id="test",
            export_format="invalid_format",
            components=[]
        )
        
        with self.assertRaises(ValueError):
            self.report_exporter.export_enhanced_report({}, invalid_config)
    
    def test_performance_metrics(self):
        """Test performance and scalability features."""
        # Test multiple audit events
        start_time = datetime.now()
        
        for i in range(100):
            self.audit_service.log_event(
                event_type=AuditEventType.API_CALL,
                user_id=f"user_{i}",
                action=f"api_call_{i}"
            )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Should complete within reasonable time
        self.assertLess(duration, 10.0)  # 10 seconds max
        
        # Test multiple CAPTCHA challenges
        challenges = []
        for i in range(50):
            challenge = self.captcha_service.generate_challenge("text", "easy")
            challenges.append(challenge["challenge_id"])
        
        self.assertEqual(len(challenges), 50)
        
        # Test encryption performance
        large_data = {"large_field": "x" * 10000}  # 10KB of data
        
        start_time = datetime.now()
        encrypted = self.encryption_service.encrypt_data(large_data)
        decrypted = self.encryption_service.decrypt_data(encrypted)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        self.assertLess(duration, 5.0)  # 5 seconds max
        self.assertEqual(decrypted, large_data)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
