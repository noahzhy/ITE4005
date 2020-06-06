/**
 * Item data 
 *
 * @author      Kwangil Cho
 * @since       2017-06-05
 * @file        item.h
 */
#ifndef __ASSIGNMENT4_INCLUDE_ITEM_H__
#define __ASSIGNMENT4_INCLUDE_ITEM_H__
#define NUM_GENRE 19
#include <bitset>
#include <vector>

struct item {
    std::bitset<NUM_GENRE> *genre;
};

extern int NUM_ITEM;
extern vector<struct item> g_items;
#endif // __ASSIGNMENT4_INCLUDE_ITEM_H__
