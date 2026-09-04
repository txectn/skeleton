import hashlib

class FingerprintService:

    @staticmethod
    def create(*, data):
        fingerprint_data = "|".join([
            data.get("device_id", ""),
            data.get("user_agent", ""),
            data.get("browser", ""),
            data.get("browser_version", ""),
            data.get("operating_system", ""),
            data.get("os_version", ""),
            data.get("device_type", ""),
        ])

        return hashlib.sha256(
            fingerprint_data.encode("utf-8")
        ).hexdigest()