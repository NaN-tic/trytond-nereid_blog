#This file is part nereid_blog module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.pool import Pool
from .blog import *


def register():
    Pool.register(
        Category,
        Post,
        PostCategory,
        PostImage,
        module='nereid_blog', type_='model')
