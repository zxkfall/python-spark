from pyspark import SparkConf, SparkContext
import os

if __name__ == '__main__':
    print(os.path.dirname(__file__))
    conf = (SparkConf().setAppName('wordCount')
            .setMaster("spark://localhost:7077")
            )  # 使用 Docker 主机 IP
            # .setMaster("local"))  # 本地运行

    sc = SparkContext(conf=conf)

    # 确保文件路径正确 --important!!!
    data = sc.textFile("hdfs://172.18.0.5:8020/wd.txt")

    output = data \
        .flatMap(lambda line: line.split(' ')) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda line: line[1], False) \
        .collect()

    for word, count in output:
        print("{}\t{}".format(word, count))

    sc.stop()
