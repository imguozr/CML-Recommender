import numpy as np
from scipy.sparse import dok_matrix, lil_matrix
from tqdm import tqdm


def goodbooks():
    user_set = set([])
    item_set = set([])
    user_max = 0
    item_max = 0
    for u, item_list in enumerate(open('goodbooks-10k/ratings.csv').readlines()):
        items = item_list.strip().split(",")
        if items[0] != 'user_id':
            user_id = int(items[0])
            item_id = int(items[1])
            user_set.add(user_id)
            item_set.add(item_id)
            if item_id > item_max:
                item_max = item_id
            if user_id > user_max:
                user_max = user_id
            if len(user_set) == 2000:
                break

    n_users = user_max + 1
    n_items = item_max + 1

    user_item_matrix = dok_matrix((n_users, n_items), dtype=np.int32)

    for u, item_list in enumerate(open('goodbooks-10k/ratings.csv').readlines()):
        items = item_list.strip().split(",")
        if items[0] != 'user_id':
            user_id = int(items[0])
            item_id = int(items[1])
            rating = int(items[2])
            if user_id not in user_set:
                break
            user_item_matrix[user_id, item_id] = rating

    return user_item_matrix


def split_data(user_item_matrix, split_ratio=(3, 1, 1), seed=1):
    # set the seed to have deterministic results
    np.random.seed(seed)
    train = dok_matrix(user_item_matrix.shape)
    validation = dok_matrix(user_item_matrix.shape)
    test = dok_matrix(user_item_matrix.shape)
    # convert it to lil format for fast row access
    user_item_matrix = lil_matrix(user_item_matrix)
    for user in tqdm(range(user_item_matrix.shape[0]), desc="Split data into train/valid/test"):
        items = list(user_item_matrix.rows[user])
        if len(items) >= 5:

            np.random.shuffle(items)

            train_count = int(len(items) * split_ratio[0] / sum(split_ratio))
            valid_count = int(len(items) * split_ratio[1] / sum(split_ratio))

            for i in items[0: train_count]:
                train[user, i] = 1
            for i in items[train_count: train_count + valid_count]:
                validation[user, i] = 1
            for i in items[train_count + valid_count:]:
                test[user, i] = 1
    print("{}/{}/{} train/valid/test samples".format(
        len(train.nonzero()[0]),
        len(validation.nonzero()[0]),
        len(test.nonzero()[0])))

    return train, validation, test
