/**
 * User data
 *
 * @author      Kwangil Cho
 * @since       2017-06-05
 * @file        user.h
 */
#ifndef __ASSIGNMENT4_INCLUDE_UESR_H__
#define __ASSIGNMENT4_INCLUDE_UESR_H__
#define NUM_GENRE 19
#include <vector>
using namespace std;

struct user {
    char age; // Young: ~20 Mature:21~55 Old: 56~
    bool gender; // Male: 1 Female: 0
    int job; // translated into int from string by jobmap

    double favor[NUM_GENRE] = {0};
    int favor_cnt[NUM_GENRE] = {0};
    int top5[5];
};

extern int NUM_USER;
extern vector<struct user> g_users;
#endif // __ASSIGNMENT4_INCLUDE_UESR_H__
