import argparse
import sys
from utils.query_search import get_seo_related_in_ranks

# defining switches
## seo check
parser = argparse.ArgumentParser()

parser.add_argument('--seo-check', action="store_true", default=False)
parser.add_argument('--kw-path', required='--seo-check' in sys.argv, type=str)
# this was a good idea to use required with sys.argv # Greaaaaat


args = parser.parse_args()
# running the tool:

if __name__ == "__main__":
    print("this tool has been written by zerobits01")
    if args.seo_check:
        get_seo_related_in_ranks(
            args.kw_path
        )