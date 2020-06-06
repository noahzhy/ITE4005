/**
 * Predict the rating of item from test file
 *
 * @author      Kwangil Cho
 * @since       2017-06-05
 * @file        rate.cc
 */
#include "recommender.h"
#include "user.h" 
#include "item.h" 
#include <cmath>

/**
 * Print the predicted rating of target item into output file
 *
 * @param[in]   user_id   who evaluates the item rating
 * @param[in]   item_id   evaluating item
 * @param[in]   rating    evaluated rating by recommender system 
 */
void PrintPredictedRating(int user_id, int item_id, int rating) {
    g_fs_prediction << user_id << "\t" << item_id << "\t"
                    << rating << "\t" << endl;
}

/**
 * Evaluate(Predict) the rating of items from test file
 */
void RateTestData() {
    g_fs_test.open(PATH_TEST_DATA, ifstream::in);
    if (g_fs_test.is_open() == false) {
        cout << "Can't open test file. Program terminated." << endl;
        exit(0);
    }

    g_fs_prediction.open(PATH_PREDICTION_DATA, ofstream::out);
    if (g_fs_prediction.is_open() == false) {
        cout << "Can't open prediction file. Program terminated." << endl;
        exit(0);
    }

    int user_id;
    int item_id;
    int rating;
    int timestamp;
    while (g_fs_test >> user_id >> item_id >> rating >> timestamp) {
        /* predict the rating by Factorized rating matrix */
        rating = round(g_rating_matrix[user_id][item_id]);
        PrintPredictedRating(user_id, item_id, rating);
    }

    g_fs_test.close();
    g_fs_prediction.close();
}
