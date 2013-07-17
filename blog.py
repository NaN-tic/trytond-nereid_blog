#This file is part nereid_blog module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from string import Template

from nereid import render_template, current_app, cache, request
from nereid.helpers import slugify, url_for, key_from_list
from nereid.contrib.pagination import Pagination
from nereid.contrib.sitemap import SitemapIndex, SitemapSection
from werkzeug.exceptions import NotFound, InternalServerError

from trytond.pyson import Eval, Not, Equal, Bool, In
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pool import Pool

__all__ = ['Category', 'Post', 'PostCategory', 'PostImage']


class Category(ModelSQL, ModelView):
    "Blog Categoies"
    __name__ = 'nereid.blog.category'
    _rec_name = 'title'

    per_page = 10

    title = fields.Char('Title', size=100, translate=True,
        required=True, on_change=['title', 'uri'])
    uri = fields.Char('URI', required=True,
        help='Unique Name is used as the uri.')
    status = fields.Boolean('Status',
        help='Dissable to not show posts in this category')
    description = fields.Text('Description', translate=True)
    template = fields.Char('Template', required=True)

    @staticmethod
    def default_status():
        'Return True'
        return True

    @staticmethod
    def default_template():
        return 'blog-category.jinja'

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        cls._sql_constraints += [
            ('uri', 'UNIQUE(uri)',
                'The Unique Name of the Category must be unique.'),
            ]
        cls._error_messages.update({
            'delete_categories': ('You can not delete '
                'categories because you will get error 404 NOT Found. '
                'Dissable active field.'),
            })

    @classmethod
    def copy(cls, categories, default=None):
        new_categories = []
        for category in categories:
            default['uri'] = '%s-copy' % category.uri
            new_category, = super(Category, cls).copy([category], default=default)
            new_categories.append(new_category)
        return new_categories

    @classmethod
    def delete(cls, categories):
        cls.raise_user_error('delete_categories')

    def on_change_title(self):
        res = {}
        if self.title and not self.uri:
            res['uri'] = slugify(self.title)
        return res

    @classmethod
    def all(cls):
        """
        Renders alls
        """
        Post = Pool().get('nereid.blog.post')

        page = request.args.get('page', 1, int)
        clause = []
        clause.append(('status', '=', True))

        posts = Pagination(
            Post, clause, page, cls.per_page
        )

        return render_template('blog-all.jinja', posts=posts)

    @classmethod
    def render(cls, uri):
        """
        Renders the category
        """
        Post = Pool().get('nereid.blog.post')

        clause = []
        posts = None
        page = request.args.get('page', 1, int)

        # Find in cache or load from DB
        try:
            category, = cls.search([('uri', '=', uri)])
        except ValueError:
            return NotFound()

        clause.append(('categories', 'in', [category.id]))
        clause.append(('status', '=', True))

        if category.status:
            posts = Pagination(
                Post, clause, page, cls.per_page
            )

        return render_template(
            category.template, category=category, posts=posts)

    @classmethod
    def tag(cls, uri):
        """
        Renders by tag
        """
        Post = Pool().get('nereid.blog.post')

        page = request.args.get('page', 1, int)

        clause = []
        clause.append(('metakeywords', 'ilike', '%%%s%%' % uri))
        clause.append(('status', '=', True))

        posts = Pagination(
            Post, clause, page, cls.per_page
        )

        return render_template('blog-tag.jinja', tag=uri, posts=posts)

    def get_absolute_url(self, **kwargs):
        return url_for(
            'nereid.blog.category.render', uri=self.uri, **kwargs
        )


class Post(ModelSQL, ModelView):
    "Blog Post"
    __name__ = 'nereid.blog.post'
    _rec_name = 'uri'
    _order_name = 'published_on'
    title = fields.Char('Title', size=100, translate=True,
        required=True, on_change=['title', 'uri'])
    uri = fields.Char('URI', required=True,
        help='Unique Name is used as the uri.')
    description = fields.Text('Description', required=True, translate=True)
    metadescription = fields.Char('Meta Description', translate=True, 
        help='Almost all search engines recommend it to be shorter ' \
        'than 155 characters of plain text')
    metakeywords = fields.Char('Meta Keywords',  translate=True,
        help='Separated by comma')
    metatitle = fields.Char('Meta Title',  translate=True)
    template = fields.Char('Template', required=True)
    status = fields.Boolean('Status',
        help='Dissable to not show content post')
    categories = fields.Many2Many('nereid.blog.post-nereid.blog.category', 
        'post', 'category', 'Categories')
    images = fields.Many2Many('nereid.blog.post-image', 
        'post', 'image', 'Images')
    author = fields.Many2One('company.employee', 'Author')
    published_on = fields.Date('Published On')

    @staticmethod
    def default_status():
        return True

    def on_change_title(self):
        res = {}
        if self.title and not self.uri:
            res['uri'] = slugify(self.title)
        return res

    @staticmethod
    def default_template():
        return 'blog-post.jinja'

    @staticmethod
    def default_author():
        User = Pool().get('res.user')

        context = Transaction().context
        if context is None:
            context = {}
        employee_id = None
        if context.get('employee'):
            employee_id = context['employee']
        else:
            user = User(Transaction().user)
            if user.employee:
                employee_id = user.employee.id
        if employee_id:
            return employee_id
        return False

    @staticmethod
    def default_published_on():
        Date = Pool().get('ir.date')
        return Date.today()

    @classmethod
    def __setup__(cls):
        super(Post, cls).__setup__()
        cls._order.insert(0, ('published_on', 'DESC'))
        cls._order.insert(1, ('id', 'DESC'))
        cls._sql_constraints += [
            ('uri', 'UNIQUE(uri)',
                'The Unique Name of the Category must be unique.'),
            ]
        cls._error_messages.update({
            'delete_posts': ('You can not delete '
                'posts because you will get error 404 NOT Found. '
                'Dissable active field.'),
            })

    @classmethod
    def copy(cls, posts, default=None):
        new_posts = []
        for post in posts:
            default['uri'] = '%s-copy' % post.uri
            new_post, = super(Post, cls).copy([post], default=default)
            new_posts.append(new_post)
        return new_posts

    @classmethod
    def delete(cls, posts):
        cls.raise_user_error('delete_posts')

    @classmethod
    def render(cls, uri):
        """
        Renders the template
        """
        try:
            post, = cls.search([('uri', '=', uri)])
        except ValueError:
            return NotFound()
        return render_template(post.template, post=post)

    def get_absolute_url(self, **kwargs):
        return url_for(
            'nereid.blog.post.render', uri=self.uri, **kwargs
        )


class PostCategory(ModelSQL):
    'Nereid Blog Post - Category'
    __name__ = 'nereid.blog.post-nereid.blog.category'
    _table = 'nereid_blog_post_category'

    post = fields.Many2One('nereid.blog.post', 'Post', ondelete='CASCADE',
            select=True, required=True)
    category = fields.Many2One('nereid.blog.category', 'Category', ondelete='RESTRICT',
            select=True, required=True)


class PostImage(ModelSQL):
    'Nereid Blog Post - Image'
    __name__ = 'nereid.blog.post-image'
    _table = 'nereid_blog_post_image'

    post = fields.Many2One('nereid.blog.post', 'Post', ondelete='CASCADE',
            select=True, required=True)
    image = fields.Many2One('nereid.static.file', 'Image', ondelete='RESTRICT',
            select=True, required=True)
