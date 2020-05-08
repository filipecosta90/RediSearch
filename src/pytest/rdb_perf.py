import os
import subprocess
import time

from includes import *
from redis.client import parse_info
TEST20 = os.environ.get("TEST20") == "1"

REDISEARCH_CACHE_DIR = '/tmp/'
BASE_RDBS_URL = 'https://performance-cto-group-public.s3.amazonaws.com/benchmarks/redisearch/ftsb/rdbs/'

RDBS = {
    "synthetic-numeric-int-idx1": 'redisearch-load-synthetic-numeric-int_1M_docs.rdb',
    "synthetic-tag-idx1": 'redisearch-load-synthetic-tag_1M_docs.rdb',
    "synthetic-text-idx1": 'redisearch-load-synthetic-text_1M_docs.rdb',
    "enwiki-abstract-idx1": 'enwiki-abstract-601164_docs.rdb',
}

if TEST20:
    RDBS = {
        "2.0-ynthetic-numeric-int-idx1": '2.0-redisearch-load-synthetic-numeric-int_1M_docs.rdb',
        "2.0-synthetic-tag-idx1": '2.0-redisearch-load-synthetic-tag_1M_docs.rdb',
        "2.0-synthetic-text-idx1": '2.0-redisearch-load-synthetic-text_1M_docs.rdb',
        "2.0-enwiki-abstract-idx1": '2.0-enwiki-abstract-601164_docs.rdb',
    }

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if abs(num) < 1000.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def downloadFiles():
    if not os.path.exists(REDISEARCH_CACHE_DIR):
        os.makedirs(REDISEARCH_CACHE_DIR)
    for f in RDBS.values():
        path = os.path.join(REDISEARCH_CACHE_DIR, f)
        if not os.path.exists(path):
            subprocess.call(['wget', BASE_RDBS_URL + f, '-O', path])
        if not os.path.exists(path):
            return False
    return True


def get_run_skeleton():
    return {'byte_rate_humanfmt': None, 'used_memory_humanfmt': None, 'byte_rate': None, 'used_memory': None,
            'elapsed_time': None}


def testRDBLoadSpeed(env):
    env.skipOnCluster()
    dbFileName = env.cmd('config', 'get', 'dbfilename')[1]
    dbDir = env.cmd('config', 'get', 'dir')[1]
    rdbFilePath = os.path.join(dbDir, dbFileName)
    if not downloadFiles():
        if os.environ.get('CI'):
            env.assertTrue(False)  ## we could not download rdbs and we are running on CI, let fail the test
        else:
            env.skip()
            return

    rdb_bw_stats = {}
    for idx_name in RDBS.keys():
        rdb_bw_stats[idx_name] = []

    for idxName, fileName in RDBS.items():
        env.stop()
        filePath = os.path.join(REDISEARCH_CACHE_DIR, fileName)
        try:
            os.unlink(rdbFilePath)
        except OSError:
            pass
        os.symlink(filePath, rdbFilePath)
        t = time.time()
        env.start()
        elapsed_time = time.time() - t
        used_memory = parse_info(env.cmd('info memory'))['used_memory']
        byte_rate = used_memory / elapsed_time
        run_info = {'byte_rate_humanfmt': None, 'used_memory_humanfmt': None, 'byte_rate': None, 'used_memory': None,
                    'elapsed_time': None}
        run_info['byte_rate'] = byte_rate
        run_info['byte_rate_humanfmt'] = sizeof_fmt(byte_rate)
        run_info['used_memory'] = used_memory
        run_info['used_memory_humanfmt'] = sizeof_fmt(used_memory)
        run_info['elapsed_time'] = elapsed_time
        rdb_bw_stats[idxName].append(run_info)
        env.assertTrue(env.checkExitCode())
    env.debugPrint("{:30}\t{:15}\t{:20}\t{:15}".format("Index","Index Size","RDB Load time(sec)","RDB Load Byte Rate"), True)

    for idxName, result_group in rdb_bw_stats.items():
        if len(result_group) > 0:
            # TODO: run each test more than once and report best
            best_result = result_group[0]
            env.debugPrint( "{:30}\t{:15}\t{:18.2f}\t{:>15}/sec".format(idxName,best_result["used_memory_humanfmt"],best_result["elapsed_time"], best_result["byte_rate_humanfmt"]), True)


if __name__ == "__main__":
    if not downloadFiles():
        raise Exception("Couldn't download RDB files")
    print("RDB Files ready for testing!")
