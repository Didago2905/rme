from services.logger_service import LoggerService


def test_logger_service():
    logger = LoggerService()

    logger.info(
        "Analyzer started"
    )

    logger.info(
        "File analyzed successfully"
    )

    logger.error(
        "Test error message"
    )

    print(
        "Logs written"
    )


if __name__ == "__main__":
    test_logger_service()