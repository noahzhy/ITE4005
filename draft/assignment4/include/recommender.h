/**
 * Contains program-wide variables
 *
 * @author      Kwangil Cho
 * @since       2017-06-05
 * @file        recommender.h
 */
#ifndef __ASSIGNMENT4_INCLUDE_RECOMMENDATION_SYSTEM_H__
#define __ASSIGNMENT4_INCLUDE_RECOMMENDATION_SYSTEM_H__

#include <iostream>
#include <fstream>
#define NUM_GENRE 19
using namespace std;

extern double **g_rating_matrix;
extern double **g_user_sim_matrix;

extern fstream g_fs_test;
extern ofstream g_fs_prediction;

extern string PATH_ROOT_DIR;
extern string PATH_TRAINING_DATA;
extern string PATH_TEST_DATA;
extern string PATH_PREDICTION_DATA;
extern string PREDICTION_POSTFIX;

extern string INFO_FILE_NAME;
extern string ITEM_FILE_NAME;
extern string USER_FILE_NAME;
extern string JOB_FILE_NAME;
#endif // __ASSIGNMENT4_INCLUDE_RECOMMENDATION_SYSTEM_H__
