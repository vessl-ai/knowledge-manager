


import json

from config import get_config
from ingester import IngestRunner


def main(**kwargs):
    # Set the default configuration
    config = get_config()
    print(json.dumps(config.__dict__(), indent=4))
    runner = IngestRunner(config)

    runner.run()


if __name__ == "__main__":
    main()