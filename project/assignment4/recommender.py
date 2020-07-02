import os, argparse
import numpy as np
import pandas as pd


class UserCF:
    def __init__(self, train_data):
        self.train = train_data
        self.n_users = max(self.train.iloc[:, 0].unique())
        self.n_items = max(self.train.iloc[:, 1].unique())
        self.rating_mat = np.full((self.n_users, self.n_items), -1)
        self.avg_rating = np.zeros(self.n_users)
        self.user_sim_mat = np.ones([self.n_users, self.n_users])

        for user_id, item_id, rating, _ in self.train.values.tolist():
            self.rating_mat[user_id-1][item_id-1] = rating

        for user in range(self.n_users):
            rated_item = (self.rating_mat[user] >= 0)
            self.avg_rating[user] = self.rating_mat[user][rated_item].sum() / len(rated_item[rated_item])

        for i in range(self.n_users):
            for j in range(self.n_users):
                self.user_sim_mat[i][j] = self.cosine(self.rating_mat[i], self.rating_mat[j])

    @staticmethod
    def cosine(vec1, vec2):
        mat_a, mat_b = np.mat(vec1), np.mat(vec2)
        denom = np.linalg.norm(mat_a) * np.linalg.norm(mat_b)
        return (0.5 + 0.5 * (float(mat_a * mat_b.T) / denom))

    def predict(self, test_data):
        res = list()
        for user_id, item_id, _, _ in test_data.values.tolist():
            user, item = user_id-1, item_id-1
            try:
                item_info = self.rating_mat[:, item]
                rated = (item_info >= 0)
                rated_user_sim = self.user_sim_mat[user, rated]
                if rated_user_sim.sum() == 0:
                    res.append([user_id, item_id, self.avg_rating[user]])
                else:
                    user_sim_ratings = rated_user_sim * (item_info[rated] - self.avg_rating[rated])
                    rating = self.avg_rating[user] + user_sim_ratings.sum() / rated_user_sim.sum()
                    res.append([user_id, item_id, np.clip(rating, 1, 5)])
            except IndexError as e:
                res.append([user_id, item_id, self.avg_rating[user]])
        return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("train", type=str)
    parser.add_argument("test", type=str)
    args = parser.parse_args()

    train_data = pd.read_table(args.train, index_col=None, header=None)
    test_data = pd.read_table(args.test, index_col=None, header=None)

    np.savetxt(
        "{}.base_prediction.txt".format(os.path.splitext(os.path.basename(args.train))[0]),
        list(UserCF(train_data).predict(test_data)),
        fmt='%d\t%d\t%s'
    )
