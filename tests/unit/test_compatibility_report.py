from core.models.compatibility_report import CompatibilityReport


def test_compatibility_report_creation():
    report = CompatibilityReport(
        is_compatible=False,
        profile_name="web_safe",
        score=65,
        issues=[
            "Video codec not supported",
            "Subtitle codec not supported",
        ],
    )

    print(report)


if __name__ == "__main__":
    test_compatibility_report_creation()