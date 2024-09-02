


from jobs.ingester.src.config import get_config
from jobs.ingester.src.ingester import IngestRunner


def main(**kwargs):
    # Set the default configuration
    config = get_config()
    runner = IngestRunner(config)

    runner.run()
