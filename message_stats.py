#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 23
@author: Hanna
"""


import matplotlib.pyplot as plt
import emoji
import pandas as pd
import numpy as np



def is_emoji(char):
    """extracts all emojis from text """
    # emoji_list = []
    # for c in char:
    #     if c in emoji.UNICODE_EMOJI:
    #         emoji_list.append(c)
    # if emoji_list:
    #     return True
    if char in emoji.UNICODE_EMOJI:
        return True
  


def get_chat_messages(text, names):
    """
    input: txt file with WhatsApp messages,
                list of names of people in the chat group
    """
    #dictionary with tokenized messages
    messages = {}
    for n in names:
        messages[n] = []
    #assign messages to names and save in dictionary
    for l in text:
        words = l.split()
        try:
            name = words[3][:-1]
            try:
                for m in words[4:]:
                    messages[name].append(m)
            except KeyError:
                continue
        except IndexError:
            continue

    return messages


def get_message_counts(text, names):
    """count number of messages for each chat member"""
    #dictionary with message counts
    counts, words = dict(), dict()
    for n in names:
        counts[n] = 0
        words[n] = 0

    for m in text:
        try:
            name = m.split()[3][:-1]
            num_words = len(m.split()[4:])
            if name in counts.keys():
                counts[name] += 1
                words[name] += num_words
        except IndexError:
            continue
    #return counts for message counts
    return counts
    #return words for word counts
    #return words




def visualize_message_freqs(message_counts):
    """plot a bar chart of number of messages per chat member"""
    names, counts = list(), list()
    for k,v in message_counts.items():
        names.append(k)
        counts.append(v)

    y_pos = np.arange(len(names))

    plt.bar(y_pos, counts, align='center', alpha=0.3)
    plt.xticks(y_pos, names)
    plt.ylabel('Count')
    plt.title('Message count per person')

    plt.show()





def extract_emojis(messages):
    """
    argument: dictionary of messages assigned to names
    """
    emoji_dict = {}
    for name in messages.keys():
        emoji_dict[name] = {}
    #get emojis from messages and add to emoji dictionary
    for name, mess in messages.items():
        for char in mess:
            if is_emoji(char):
                print(char)
                if char not in emoji_dict[name]:
                    emoji_dict[name][char] = 1
                else:
                    emoji_dict[name][char] += 1

    return emoji_dict



def top_n_emojis(emoji_dict, n):
    """
    argument: dictionary of emojis and absolute counts assigned to names,
              int n (number of emojis you are interested in)
    """
    top_emojis = {}
    for name in emoji_dict.keys():
        top_emojis[name] = {}
    #get top n emojis
    for name, emos in emoji_dict.items():
        top_emos = sorted(emos, key=emos.__getitem__, reverse=True)[:n]
        for e in top_emos:
            top_emojis[name][e] = emoji_dict[name][e]

    return top_emojis



def relative_counts(top_emojis):
    """calculate percentages
    """
    frequencies = {}
    for name in top_emojis.keys():
        frequencies[name] = {}
    #calculate relative counts for all top emojis for each chat member
    for name, emos in top_emojis.items():
        emos_count = sum(emos.values())
        for e in emos:
            frequencies[name][e] = round(top_emojis[name][e]/emos_count*100, 2)

    return frequencies



def visualize_top_emojis(frequencies):
    """visualize the distribution of emojis among chat participants using matplotlib
    """

    for name, emos in frequencies.items():
        emojis = []
        freqs = []
        for e,f in emos.items():
            emojis.append(e)
            freqs.append(f)
        df = pd.DataFrame({'chars': emojis, 'num': freqs})
        axis = df.plot.bar()
        plt.show()
        return emojis



        
def main(file, names):
    text = list()
    with open(file, "rt") as f:
        for l in f:
            text.append(l)
    counts = get_message_counts(text, names)
    print(counts)
    visualize_message_freqs(counts)
    #messages = get_chat_messages(text, names)
    #emo_d = extract_emojis(messages)
    #top = top_n_emojis(emo_d, 5)
    #freqs = relative_counts(top)
    #print(visualize_top_emojis(freqs))



    

if __name__ == '__main__':
    main("chat.txt", ("Leni", "Rhonda", "Hanna"))

