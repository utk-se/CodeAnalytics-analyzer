import exceptions
import statistics
from collections import Counter
from sklearn.cluster import KMeans


sampling_methods = {
    'mode': statistics.mode,
    'median': statistics.median
}


class AggregationException(BaseException):
    pass


def sortkey_linecollection(lc):
    return len(lc['line_objs'])


def sortkey_linelist(line):
    return line['start_index']

# evenly split a list into n chunks


def to_chunk(l, n_chunks):
    # len(chunk) == len(list) // n_chunks
    return [l[i:i + len(l) // n_chunks] for i in range(0, len(l), len(l) // n_chunks)]

# python's statistics mode sucks, it doesn't support key and throws an
# exception if there's two equally common values


def freq(line_container, asarray=False):
    # TODO: refactor for linecontainer
    line_freqs = []
    # get max
    max_lines = max(line_container, key=sortkey_linecollection)
    # frequency count across each collection of lines
    if line_num >= self.repo_obj['max_file_length']:

        line_freq_obj = {
            "start_indexes": {
                line_obj["start_index"]: 1
            },
            "end_indexes": {
                line_obj["end_index"]: 1
            },
            "num_tabs": line_obj["num_tabs"],
            "num_spaces": line_obj["num_spaces"],
        }
        self.repo_obj["line_freqs"].append(
            line_freq_obj)
    else:
        if line_obj["start_index"] not in self.repo_obj["line_freqs"][line_num]["start_indexes"].keys():
            self.repo_obj["line_freqs"][line_num]["start_indexes"][line_obj["start_index"]] = 1
        else:
            self.repo_obj["line_freqs"][line_num]["start_indexes"][line_obj["start_index"]] += 1

        if line_obj["end_index"] not in self.repo_obj["line_freqs"][line_num]["end_indexes"].keys():
            self.repo_obj["line_freqs"][line_num]["end_indexes"][line_obj["start_index"]] = 1
        else:
            self.repo_obj["line_freqs"][line_num]["end_indexes"][line_obj["end_index"]] += 1

        self.repo_obj["line_freqs"][line_num]["num_tabs"] += line_obj["num_tabs"]
        self.repo_obj["line_freqs"][line_num]["num_spaces"] += line_obj["num_tabs"]


def my_mode(lst):
    data_dict = dict(lst)


'''
line_obj = {
    "index": line_num,
    "start_index": None,  # int specifying where line starts
    "num_tabs": 0,  # boolean for existence
    "end_index": None,  # int specifying where line ends
    "num_spaces": 0,
    "len": 0
}
This will downscale a list of line objs
'''


def downsample(line_objs, n_chunks, method=):
    line_chunks = to_chunk(line_objs, n_chunks)
    rv_lines = []
    for i, chunk in enumerate(line_chunks):
        agg_line_obj = {
            "index": i,
            # int specifying where line starts
            "start_index": None,
            "num_tabs": 0,  # boolean for existence
            "end_index": None,  # int specifying where line ends
            "num_spaces": 0,
            "len": 0
        }
        # get mode of each thing
        # TODO: probably a much better way to do this but mode doesn't support key=?
        start_indexes = []
        num_tabs = []
        end_indexes = []
        num_spaces = []
        lens = []
        for line in chunk:
            start_indexes.append(line['start_index'])
            num_tabs.append(line['num_tabs'])
            end_indexes.append(line['end_index'])
            num_spaces.append(line['num_spaces'])
            lens.append(line['len'])

        try:
            agg_line_obj['start_index'] = method(start_indexes)

        agg_line_obj['num_tabs'] = method(num_tabs)
        agg_line_obj['end_index'] = method(end_indexes)
        agg_line_obj['num_spaces'] = method(num_spaces)
        agg_line_obj['len'] = method(lens)

        rv_lines += agg_line_obj
    return rv_lines


def scalek(line_container, k, downsampling_method='mode', upsampling_method='nearest_neighbor', merge_method=None):
    # Upscaling not supported for this dim
    if len(line_container) <= 0:
        raise AggregationException(
            "Line collection empty. have you run .analyze()?")

    if k <= 0 or k > len(line_container):
        raise AggregationException(
            "Expected 0 < k: {} < {}".format(k, len(line_container)))

    # get sampling methods
    if type(downsampling_method) is str:
        if downsampling_method in sampling_methods.keys():
            downsampling_method = sampling_methods[downsampling_method]
        else:
            raise AggregationException(
                "Invalid downsampling identifier: {}".format(downsampling_method))

    # linegroup clustering; group similarly sized linegroups into k groups.
    line_container.sort(key=sortkey_linecollection)
    line_container = to_chunk(line_container, k)
    # TODO: use k means clustering
    # k_means = KMeans(n_clusters=k, max_iter=100)
    # k_means.fit()
    # perform elementwise (line_obj) scaling on each element
    ret_collection = []

    for line_subcollection in line_container:
        # TODO: find median num_lines (will be length of our aggregated line collection)
        median_count = len(line_subcollection[len(
            line_subcollection) // 2]['line_objs'])
        # for each linegroup in subcollection, up/downscale to fit median line length
        for linegroup in line_subcollection:
            # if linegroup smaller than median, upscale
            if len(linegroup['line_objs']) < median_count:
                # use upscaling method to meet target line length
                # just add a bunch of blank lines essentially
                while len(linegroup['line_objs']) < median_count:
                    linegroup['line_objs'].append(linegroup['line_objs'][-1])
            else:
                # split lines into chunks (size of lg // chunksize) + remainder = target size
                print(len(linegroup['line_objs']))
                print(median_count)
                linegroup['line_objs'] = downsample(
                    linegroup['line_objs'], median_count)

    return line_container
