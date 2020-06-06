/**
 * Movie Recommender that predicts the rating
 * After learning from training data
 *
 * @author      Kwangil Cho
 * @since       2017-06-05
 * @file        recommender.cc
 */
#include "recommender.h"
#include "user.h"
#include "item.h"
#include <string>
#include <cstring>
#include <unordered_map>

/* global variables */
fstream g_fs_training; // training file stream
fstream g_fs_test; // test file stream
ofstream g_fs_prediction; // output file stream
ofstream g_fs_monitor; // monitoring file stream
double **g_rating_matrix; // user-item rating matrix
double **g_user_sim_matrix; // similarity between users 
static unordered_map<string, int> jobmap; // map the job(string) to int
vector<struct user> g_users; // all users
vector<struct item> g_items; // all items

/* function declarations */
static void InitPATH(const char *argv[]);
static void InitTrainingData();
static void InitInfo();
#ifdef CONTENT_BASED
static void InitUser();
static void InitItem();
#endif
static void InitRating();
void FactorizeMatrix();
void RateTestData();

/**
 * @param[in]   command line arguments as below:
 *              argv[0] executable file
 *              argv[1] training data file
 *              argv[2] test data file
 * @return      0
 */
int main(int argc, const char *argv[]) {
    if (argc == 3) {
        InitPATH(argv);
        InitTrainingData();
        FactorizeMatrix();
        RateTestData();
    } else {
        cout << "Invalid usage. Please check the arguments." << endl
           << "$ [executable file] [training file] [test file]" << endl;
    }

    return 0;
}

/**
 * Initialize the file paths with Command Line Arguments
 * 1. training data file path
 * 2. test data file path
 * 3. root directory path(based on training data)
 * 4. prediction data(output data) file path(based on training data)
 *
 * @param[in]   argv   input command line arguments 
 */
static void InitPATH(const char *argv[]) {
    PATH_TRAINING_DATA = argv[1];
    PATH_TEST_DATA = argv[2];

    int found = PATH_TEST_DATA.find_last_of('/');
    PATH_ROOT_DIR = PATH_TRAINING_DATA.substr(0, found + 1);
    PATH_PREDICTION_DATA = PATH_TRAINING_DATA + PREDICTION_POSTFIX;
}

/**
 * Initialize training data by reading and parsing the input training file
 * Initialize user, item and rating information with input training data
 */
static void InitTrainingData() {
    InitInfo();
#ifdef CONTENT_BASED
    InitUser();
    InitItem();
#endif
    InitRating();
#ifdef PRINT
    PrintRatingMatrix();
#endif
}

/**
 * Initialize number of user and number of item from info data file
 */
static void InitInfo() {
    /* initialize NUM_USER and NUM_ITEM,
     * Note the format of info data */
    string PATH = PATH_ROOT_DIR + INFO_FILE_NAME;
    g_fs_training.open(PATH, ifstream::in);
    if (g_fs_training.is_open() == false) {
        cout << "Can't open info file. Program terminated." << endl;
        std::cout << "Note: name of info file should be u.info" << std::endl;
        std::cout << "info file format:" << std::endl;
        std::cout << "first line : [# of users] users" << std::endl;
        std::cout << "second line : [# of items] items" << std::endl;
        exit(0);
    }
    
    string description;
    g_fs_training >> NUM_USER >> description;
    g_fs_training >> NUM_ITEM >> description;
    g_fs_training.close();
}

#ifdef CONTENT_BASED
/**
 * Initialize each user's job, age, gender, and occupation info
 */
static void InitUser() {
    /* initialize job info*/
    string PATH = PATH_ROOT_DIR + JOB_FILE_NAME;
    g_fs_training.open(PATH, ifstream::in);
    if (g_fs_training.is_open() == false) {
        cout << "Can't open job info file. Program terminated." << endl;
        exit(0);
    }

    /* map the job(string) to integer */
    int number = 0;
    string job;
    while (g_fs_training >> job) {
        jobmap[job] = number++;
    }
    g_fs_training.close();

    /* initialize user characteristics (age, gender and job)*/
    PATH = PATH_ROOT_DIR + USER_FILE_NAME;
    g_fs_training.open(PATH, ifstream::in);
    if (g_fs_training.is_open() == false) {
        cout << "Can't open user info file. Program terminated." << endl;
        exit(0);
    }

    struct user new_user;
    string userinfo;
    string delimiter = "|";
    size_t pos = 0;

    g_users.push_back(new_user); // dummy node, not use index 0
    while (getline(g_fs_training, userinfo)) {
        /* truncate id info */
        pos = userinfo.find(delimiter);
        userinfo.erase(0, pos + delimiter.length());

        /* set age */
        pos = userinfo.find(delimiter);
        int age = stoi(userinfo.substr(0, pos));
        userinfo.erase(0, pos + delimiter.length());

        /* set gender */
        pos = userinfo.find(delimiter);
        string gender = userinfo.substr(0, pos);
        userinfo.erase(0, pos + delimiter.length());

        /* set job */
        pos = userinfo.find(delimiter);
        string job = userinfo.substr(0, pos);

        new_user.age = age <= 20 ? 'Y' : age <= 55 ? 'M' : 'O';
        new_user.gender = gender == "M" ? 1 : 0;
        new_user.job = jobmap[job];

        /* add new user */
        g_users.push_back(new_user);
    }
    g_fs_training.close();
}

/**
 * Initialize each item's genre info
 */
static void InitItem() {
    string PATH = PATH_ROOT_DIR + ITEM_FILE_NAME;
    g_fs_training.open(PATH, ifstream::in);
    if (g_fs_training.is_open() == false) {
        cout << "Can't open item info file. Program terminated." << endl;
        exit(0);
    }

    struct item new_item;
    string iteminfo;
    string genre2bitset;
    string delimiter = "|";
    size_t pos = 0;

    g_items.push_back(new_item); // dummy node, not use index 0
    while (getline(g_fs_training, iteminfo)) {
        genre2bitset.clear();
        pos = 0;
        /* skip unnecessary information */
        for (int i = 0; i < 5; i++) {
            pos = iteminfo.find(delimiter, pos + 1);
        }
        /* truncate unnecessary information */
        iteminfo.erase(0, pos + delimiter.length());

        /* map the genre(string) to bitset */
        int len = iteminfo.length();
        for (int i = 0; i < len; i++) {
            if (iteminfo[i] != '|') {
                genre2bitset += iteminfo[i];
            }
        }
        new_item.genre = new bitset<NUM_GENRE> (genre2bitset);
        /* add new item */
        g_items.push_back(new_item);
    }
    g_fs_training.close();
}
#endif

/**
 * Initialize rating information from training data and
 * Set the rating value into user-item rating 2D matrix
 */
static void InitRating() {
    /* create a user-item rating 2D matrix */
    g_rating_matrix = (double **)malloc(sizeof(double *) * (NUM_USER + 1));
    for (int i = 1; i <= NUM_USER; i++) {
        g_rating_matrix[i] = (double *)malloc(sizeof(double) * (NUM_ITEM + 1));
        memset(g_rating_matrix[i], 0, NUM_ITEM + 1);
    }

    g_fs_training.open(PATH_TRAINING_DATA, ifstream::in);
    if (g_fs_training.is_open() == false) {
        cout << "Can't open training data file. Program terminated." << endl;
        exit(0);
    }

    int user_id;
    int item_id;
    int rating;
    int timestamp;
    while (g_fs_training >> user_id >> item_id >> rating >> timestamp) {
        /* set the rating of item evaluated by user */
        g_rating_matrix[user_id][item_id] += rating;
    }

    g_fs_training.close();
}
