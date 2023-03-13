# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:59:06 2023

@author: hzhang
"""

# color theme
COLOR_THEME = {'light': '#757ce8','main': '#3f50b5',
               'dark': '#002884', 'text': '#fff'}


# ttk theme
TTK_THEME = {"nav.TFrame" : {"background": COLOR_THEME['main']},
             "nav.TButton": {"font": ("Bahnschrift", 10), "foreground": COLOR_THEME['text'],
                            "background": COLOR_THEME['main'], "activebackground":COLOR_THEME['light']},
             "Heading.TLabel": {"font": ("Bahnschrift", 10), "foreground": COLOR_THEME['dark'] }}
