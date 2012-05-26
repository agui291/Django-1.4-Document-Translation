Models

#A model is the single, definitive source of data about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.
模型（model)是你数据来源的唯一决定性的途径,它包含了你存储的数据的关键字段和行为，通常来讲，一个模型对应着一个单独的数据库表。

#The basics:
基础知识:

#Each model is a Python class that subclasses django.db.models.Model.
#Each attribute of the model represents a database field.
#With all of this, Django gives you an automatically-generated database-access API; see Making queries.

每一个模型就是一个python"django.db.models.Model"类下面的子类。
模型的每一个属性代表了一个数据库的字段。
综合来说，Django给了你一个自动生成的数据库获取的API；参见"Making queries".

#Quick example
#This example model defines a Person, which has a first_name and last_name:
示例
这个模型的例子定义了一个"Person"的数据库表，其字段为"first_name,last_name".

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

#first_name and last_name are fields of the model. Each field is specified as a class attribute, and each attribute maps to a database column.

字段"first_name,last_name"分别是指定的类的属性，同时每一个属性对应着一个数据库表中的栏目（字段）。
上面的这段模型的代码会生成一个如下的数据库表：
#The above Person model would create a database table like this:


CREATE TABLE myapp_person (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);

#Some technical notes:

The name of the table, myapp_person, is automatically derived from some model metadata but can be overridden. See Table names for more details..
An id field is added automatically, but this behavior can be overridden. See Automatic primary key fields.
The CREATE TABLE SQL in this example is formatted using PostgreSQL syntax, but it's worth noting Django uses SQL tailored to the database backend specified in your settings file.
Using models
Once you have defined your models, you need to tell Django you're going to use those models. Do this by editing your settings file and changing the INSTALLED_APPS setting to add the name of the module that contains your models.py.

For example, if the models for your application live in the module mysite.myapp.models (the package structure that is created for an application by the manage.py startapp script), INSTALLED_APPS should read, in part:

一些技术说明：

根据模型的元数据，会生成一张名称为"myapp_person"的数据库表，这个生成行为是可覆盖原来数据库中的同名的数据库表的。
同时会自动追加一个"id"的字段，该行为同样也是可覆盖的。

使用模型
当你定义好的你的模块的时候，你需要告诉django你将要使用这个模块。你需要编辑你的setting.py文件，并在INSTALLED_APPS里加入你的模型的名字。
例如，如果你的应用程序的模型在mysite/myapp/里的时候，你需要做如下的修改：


INSTALLED_APPS = (
    #...
    'mysite.myapp',
    #...
)

#When you add new apps to INSTALLED_APPS, be sure to run manage.py syncdb.
当你在INSTALLED_APPS中添加了新的apps后，记得运行"manage.py syncdb"。


#Fields
字段
The most important part of a model -- and the only required part of a model -- is the list of database fields it defines. Fields are specified by class attributes.
模型中最重要的部分，也是模型中唯一必须的一个部分，就是这个模型中定义的数据库字段。字段是由这个类的属性来指定的。

Example:

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

#Field types
#Each field in your model should be an instance of the appropriate Field class. Django uses the field class types to determine a few things:

字段类型
模型中的每一个字段应该是字段类属性的一个实例。django使用字段类的类型来决定一些事情，比如：

#The database column type (e.g. INTEGER, VARCHAR).
#The widget to use in Django's admin interface, if you care to use it (e.g. <input type="text">, <select>).
#The minimal validation requirements, used in Django's admin and in automatically-generated forms.
#Django ships with dozens of built-in field types; you can find the complete list in the model field reference. You can easily write your own fields if Django's built-in ones don't do the trick; see Writing custom model fields.

数据库列的类型（比如 INTEGER，VARCHAR）；
Django的管理界面中的部件功能；
以及一些自动生成表格中的最低程度的验证要求；
Django内置了许多的字段类型，你甚至还可以自己定义一些字段类型；


#Field options
#Each field takes a certain set of field-specific arguments (documented in the model field reference). For example, CharField (and its subclasses) require a max_length argument which specifies the size of the VARCHAR database field used to store the data.

#There's also a set of common arguments available to all field types. All are optional. They're fully explained in the reference, but here's a quick summary of the most often-used ones:

字段选项
每一个字段包含了一系列的字段相关的参数，比如"CharField"需要一个"max_length"的参数来限定储存在数据表表中的可变字符串的最大值。
同时还有一些通常使用到的参数，

#null
#If True, Django will store empty values as NULL in the database. Default is False.
#blank
#If True, the field is allowed to be blank. Default is False.

null和blank
null:  当参数null=Ture，django允许在数据中储存一个NULL的空值，默认情况下null=False.
blank: 当参数blank=Ture，字段可以留空，默认情况下blank=False.

#Note that this is different than null. null is purely database-related, whereas blank is validation-related. If a field has blank=True, validation on Django's admin site will allow entry of an empty value. If a field has blank=False, the field will be required.

需要注意的是blank和null不同，null纯粹是数据内容相关的，然而blank是和数据验证相关，如果一个字段的blank是ture,django的管理界面的验证会允许输入一个空值，如果一个字段的blank是false，那这个字段必须要求输入一个值。


----------------------------UNDO--------------------
choices
An iterable (e.g., a list or tuple) of 2-tuples to use as choices for this field. If this is given, Django's admin will use a select box instead of the standard text field and will limit choices to the choices given.

A choices list looks like this:

YEAR_IN_SCHOOL_CHOICES = (
    (u'FR', u'Freshman'),
    (u'SO', u'Sophomore'),
    (u'JR', u'Junior'),
    (u'SR', u'Senior'),
    (u'GR', u'Graduate'),
)
The first element in each tuple is the value that will be stored in the database, the second element will be displayed by the admin interface, or in a ModelChoiceField. Given an instance of a model object, the display value for a choices field can be accessed using the get_FOO_display method. For example:

from django.db import models

class Person(models.Model):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    name = models.CharField(max_length=60)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
>>> p = Person(name="Fred Flintstone", gender="M")
>>> p.save()
>>> p.gender
u'M'
>>> p.get_gender_display()
u'Male'

----------------------------UNDO---------------------

#default
#The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.

default
default值对于一个字段，可以是一个值或者一个callable的对象，如果是callable，那么每次一个新的对象创建时，它都是callable的。

help_text
Extra "help" text to be displayed under the field on the object's admin form. It's useful for documentation even if your object doesn't have an admin form.

primary_key
如果primary_key=Ture，那这个字段就是这个模型的primary key.
如果没有指定primary_key=Ture，Django会自动添加一个整数型自动来hold住primary key,所以除非你想自定义某个字段为primary key，那么你不需要每次都设置这个参数。

#If True, this field is the primary key for the model.
#If you don't specify primary_key=True for any fields in your model, Django will automatically add an IntegerField to hold the primary key, so you don't need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior. For more, see Automatic primary key fields.

unique
如果参数值为ture，那么这个字段必须是整个数据库表中唯一的一个字段。

以上便是对一些常用的字段选项的描述，你可以在reference中找到更多的细节。

#If True, this field must be unique throughout the table.
#Again, these are just short descriptions of the most common field options. Full details can be found in the common model field option reference.




Automatic primary key fields
By default, Django gives each model the following field:

id = models.AutoField(primary_key=True)
This is an auto-incrementing primary key.

If you'd like to specify a custom primary key, just specify primary_key=True on one of your fields. If Django sees you've explicitly set Field.primary_key, it won't add the automatic id column.

Each model requires exactly one field to have primary_key=True.

Verbose field names
Each field type, except for ForeignKey, ManyToManyField and OneToOneField, takes an optional first positional argument -- a verbose name. If the verbose name isn't given, Django will automatically create it using the field's attribute name, converting underscores to spaces.

In this example, the verbose name is "person's first name":

first_name = models.CharField("person's first name", max_length=30)
In this example, the verbose name is "first name":

first_name = models.CharField(max_length=30)
ForeignKey, ManyToManyField and OneToOneField require the first argument to be a model class, so use the verbose_name keyword argument:

poll = models.ForeignKey(Poll, verbose_name="the related poll")
sites = models.ManyToManyField(Site, verbose_name="list of sites")
place = models.OneToOneField(Place, verbose_name="related place")
The convention is not to capitalize the first letter of the verbose_name. Django will automatically capitalize the first letter where it needs to.

Relationships
Clearly, the power of relational databases lies in relating tables to each other. Django offers ways to define the three most common types of database relationships: many-to-one, many-to-many and one-to-one.

Many-to-one relationships
To define a many-to-one relationship, use django.db.models.ForeignKey. You use it just like any other Field type: by including it as a class attribute of your model.

ForeignKey requires a positional argument: the class to which the model is related.

For example, if a Car model has a Manufacturer -- that is, a Manufacturer makes multiple cars but each Car only has one Manufacturer -- use the following definitions:

class Manufacturer(models.Model):
    # ...

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    # ...
You can also create recursive relationships (an object with a many-to-one relationship to itself) and relationships to models not yet defined; see the model field reference for details.

It's suggested, but not required, that the name of a ForeignKey field (manufacturer in the example above) be the name of the model, lowercase. You can, of course, call the field whatever you want. For example:

class Car(models.Model):
    company_that_makes_it = models.ForeignKey(Manufacturer)
    # ...
See also
ForeignKey fields accept a number of extra arguments which are explained in the model field reference. These options help define how the relationship should work; all are optional.

For details on accessing backwards-related objects, see the Following relationships backward example.

For sample code, see the Many-to-one relationship model example.
Many-to-many relationships
To define a many-to-many relationship, use ManyToManyField. You use it just like any other Field type: by including it as a class attribute of your model.

ManyToManyField requires a positional argument: the class to which the model is related.

For example, if a Pizza has multiple Topping objects -- that is, a Topping can be on multiple pizzas and each Pizza has multiple toppings -- here's how you'd represent that:

class Topping(models.Model):
    # ...

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
As with ForeignKey, you can also create recursive relationships (an object with a many-to-many relationship to itself) and relationships to models not yet defined; see the model field reference for details.

It's suggested, but not required, that the name of a ManyToManyField (toppings in the example above) be a plural describing the set of related model objects.

It doesn't matter which model has the ManyToManyField, but you should only put it in one of the models -- not both.

Generally, ManyToManyField instances should go in the object that's going to be edited in the admin interface, if you're using Django's admin. In the above example, toppings is in Pizza (rather than Topping having a pizzas ManyToManyField ) because it's more natural to think about a pizza having toppings than a topping being on multiple pizzas. The way it's set up above, the Pizza admin form would let users select the toppings.

See also
See the Many-to-many relationship model example for a full example.
ManyToManyField fields also accept a number of extra arguments which are explained in the model field reference. These options help define how the relationship should work; all are optional.

Extra fields on many-to-many relationships
When you're only dealing with simple many-to-many relationships such as mixing and matching pizzas and toppings, a standard ManyToManyField is all you need. However, sometimes you may need to associate data with the relationship between two models.

For example, consider the case of an application tracking the musical groups which musicians belong to. There is a many-to-many relationship between a person and the groups of which they are a member, so you could use a ManyToManyField to represent this relationship. However, there is a lot of detail about the membership that you might want to collect, such as the date at which the person joined the group.

For these situations, Django allows you to specify the model that will be used to govern the many-to-many relationship. You can then put extra fields on the intermediate model. The intermediate model is associated with the ManyToManyField using the through argument to point to the model that will act as an intermediary. For our musician example, the code would look something like this:

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
When you set up the intermediary model, you explicitly specify foreign keys to the models that are involved in the ManyToMany relation. This explicit declaration defines how the two models are related.

There are a few restrictions on the intermediate model:

Your intermediate model must contain one - and only one - foreign key to the target model (this would be Person in our example). If you have more than one foreign key, a validation error will be raised.
Your intermediate model must contain one - and only one - foreign key to the source model (this would be Group in our example). If you have more than one foreign key, a validation error will be raised.
The only exception to this is a model which has a many-to-many relationship to itself, through an intermediary model. In this case, two foreign keys to the same model are permitted, but they will be treated as the two (different) sides of the many-to-many relation.
When defining a many-to-many relationship from a model to itself, using an intermediary model, you must use symmetrical=False (see the model field reference).
Now that you have set up your ManyToManyField to use your intermediary model (Membership, in this case), you're ready to start creating some many-to-many relationships. You do this by creating instances of the intermediate model:

>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason= "Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
[<Person: Ringo Starr>]
>>> ringo.group_set.all()
[<Group: The Beatles>]
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason= "Wanted to form a band.")
>>> beatles.members.all()
[<Person: Ringo Starr>, <Person: Paul McCartney>]
Unlike normal many-to-many fields, you can't use add, create, or assignment (i.e., beatles.members = [...]) to create relationships:

# THIS WILL NOT WORK
>>> beatles.members.add(john)
# NEITHER WILL THIS
>>> beatles.members.create(name="George Harrison")
# AND NEITHER WILL THIS
>>> beatles.members = [john, paul, ringo, george]
Why? You can't just create a relationship between a Person and a Group - you need to specify all the detail for the relationship required by the Membership model. The simple add, create and assignment calls don't provide a way to specify this extra detail. As a result, they are disabled for many-to-many relationships that use an intermediate model. The only way to create this type of relationship is to create instances of the intermediate model.

The remove() method is disabled for similar reasons. However, the clear() method can be used to remove all many-to-many relationships for an instance:

# Beatles have broken up
>>> beatles.members.clear()
Once you have established the many-to-many relationships by creating instances of your intermediate model, you can issue queries. Just as with normal many-to-many relationships, you can query using the attributes of the many-to-many-related model:

# Find all the groups with a member whose name starts with 'Paul'
>>> Group.objects.filter(members__name__startswith='Paul')
[<Group: The Beatles>]
As you are using an intermediate model, you can also query on its attributes:

# Find all the members of the Beatles that joined after 1 Jan 1961
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
[<Person: Ringo Starr]
If you need to access a membership's information you may do so by directly querying the Membership model:

>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
u'Needed a new drummer.'
Another way to access the same information is by querying the many-to-many reverse relationship from a Person object:

>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
u'Needed a new drummer.'
One-to-one relationships
To define a one-to-one relationship, use OneToOneField. You use it just like any other Field type: by including it as a class attribute of your model.

This is most useful on the primary key of an object when that object "extends" another object in some way.

OneToOneField requires a positional argument: the class to which the model is related.

For example, if you were building a database of "places", you would build pretty standard stuff such as address, phone number, etc. in the database. Then, if you wanted to build a database of restaurants on top of the places, instead of repeating yourself and replicating those fields in the Restaurant model, you could make Restaurant have a OneToOneField to Place (because a restaurant "is a" place; in fact, to handle this you'd typically use inheritance, which involves an implicit one-to-one relation).

As with ForeignKey, a recursive relationship can be defined and references to as-yet undefined models can be made; see the model field reference for details.

See also
See the One-to-one relationship model example for a full example.
OneToOneField fields also accept one optional argument described in the model field reference.

OneToOneField classes used to automatically become the primary key on a model. This is no longer true (although you can manually pass in the primary_key argument if you like). Thus, it's now possible to have multiple fields of type OneToOneField on a single model.

Models across files
It's perfectly OK to relate a model to one from another app. To do this, import the related model at the top of the model that holds your model. Then, just refer to the other model class wherever needed. For example:

from geography.models import ZipCode

class Restaurant(models.Model):
    # ...
    zip_code = models.ForeignKey(ZipCode)
Field name restrictions
Django places only two restrictions on model field names:

A field name cannot be a Python reserved word, because that would result in a Python syntax error. For example:

class Example(models.Model):
    pass = models.IntegerField() # 'pass' is a reserved word!
A field name cannot contain more than one underscore in a row, due to the way Django's query lookup syntax works. For example:

class Example(models.Model):
    foo__bar = models.IntegerField() # 'foo__bar' has two underscores!
These limitations can be worked around, though, because your field name doesn't necessarily have to match your database column name. See the db_column option.

SQL reserved words, such as join, where or select, are allowed as model field names, because Django escapes all database table names and column names in every underlying SQL query. It uses the quoting syntax of your particular database engine.

Custom field types
If one of the existing model fields cannot be used to fit your purposes, or if you wish to take advantage of some less common database column types, you can create your own field class. Full coverage of creating your own fields is provided in Writing custom model fields.

Meta options
Give your model metadata by using an inner class Meta, like so:

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
Model metadata is "anything that's not a field", such as ordering options (ordering), database table name (db_table), or human-readable singular and plural names (verbose_name and verbose_name_plural). None are required, and adding class Meta to a model is completely optional.

A complete list of all possible Meta options can be found in the model option reference.

Model methods
Define custom methods on a model to add custom "row-level" functionality to your objects. Whereas Manager methods are intended to do "table-wide" things, model methods should act on a particular model instance.

This is a valuable technique for keeping business logic in one place -- the model.

For example, this model has a few custom methods:

from django.contrib.localflavor.us.models import USStateField

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField() # Yes, this is America-centric...

    def baby_boomer_status(self):
        "Returns the person's baby-boomer status."
        import datetime
        if datetime.date(1945, 8, 1) <= self.birth_date <= datetime.date(1964, 12, 31):
            return "Baby boomer"
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        return "Post-boomer"

    def is_midwestern(self):
        "Returns True if this person is from the Midwest."
        return self.state in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)
The last method in this example is a property.

The model instance reference has a complete list of methods automatically given to each model. You can override most of these -- see overriding predefined model methods, below -- but there are a couple that you'll almost always want to define:

__unicode__()
A Python "magic method" that returns a unicode "representation" of any object. This is what Python and Django will use whenever a model instance needs to be coerced and displayed as a plain string. Most notably, this happens when you display an object in an interactive console or in the admin.

You'll always want to define this method; the default isn't very helpful at all.

get_absolute_url()
This tells Django how to calculate the URL for an object. Django uses this in its admin interface, and any time it needs to figure out a URL for an object.

Any object that has a URL that uniquely identifies it should define this method.

Overriding predefined model methods
There's another set of model methods that encapsulate a bunch of database behavior that you'll want to customize. In particular you'll often want to change the way save() and delete() work.

You're free to override these methods (and any other model method) to alter behavior.

A classic use-case for overriding the built-in methods is if you want something to happen whenever you save an object. For example (see save() for documentation of the parameters it accepts):

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something()
        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
        do_something_else()
You can also prevent saving:

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        if self.name == "Yoko Ono's blog":
            return # Yoko shall never have her own blog!
        else:
            super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
It's important to remember to call the superclass method -- that's that super(Blog, self).save(*args, **kwargs) business -- to ensure that the object still gets saved into the database. If you forget to call the superclass method, the default behavior won't happen and the database won't get touched.

It's also important that you pass through the arguments that can be passed to the model method -- that's what the *args, **kwargs bit does. Django will, from time to time, extend the capabilities of built-in model methods, adding new arguments. If you use *args, **kwargs in your method definitions, you are guaranteed that your code will automatically support those arguments when they are added.

Overriding Delete
Note that the delete() method for an object is not necessarily called when deleting objects in bulk using a QuerySet. To ensure customized delete logic gets executed, you can use pre_delete and/or post_delete signals.
Executing custom SQL
Another common pattern is writing custom SQL statements in model methods and module-level methods. For more details on using raw SQL, see the documentation on using raw SQL.

Model inheritance
Model inheritance in Django works almost identically to the way normal class inheritance works in Python. The only decision you have to make is whether you want the parent models to be models in their own right (with their own database tables), or if the parents are just holders of common information that will only be visible through the child models.

There are three styles of inheritance that are possible in Django.

Often, you will just want to use the parent class to hold information that you don't want to have to type out for each child model. This class isn't going to ever be used in isolation, so Abstract base classes are what you're after.
If you're subclassing an existing model (perhaps something from another application entirely) and want each model to have its own database table, Multi-table inheritance is the way to go.
Finally, if you only want to modify the Python-level behavior of a model, without changing the models fields in any way, you can use Proxy models.
Abstract base classes
Abstract base classes are useful when you want to put some common information into a number of other models. You write your base class and put abstract=True in the Meta class. This model will then not be used to create any database table. Instead, when it is used as a base class for other models, its fields will be added to those of the child class. It is an error to have fields in the abstract base class with the same name as those in the child (and Django will raise an exception).

An example:

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
The Student model will have three fields: name, age and home_group. The CommonInfo model cannot be used as a normal Django model, since it is an abstract base class. It does not generate a database table or have a manager, and cannot be instantiated or saved directly.

For many uses, this type of model inheritance will be exactly what you want. It provides a way to factor out common information at the Python level, whilst still only creating one database table per child model at the database level.

Meta inheritance
When an abstract base class is created, Django makes any Meta inner class you declared in the base class available as an attribute. If a child class does not declare its own Meta class, it will inherit the parent's Meta. If the child wants to extend the parent's Meta class, it can subclass it. For example:

class CommonInfo(models.Model):
    ...
    class Meta:
        abstract = True
        ordering = ['name']

class Student(CommonInfo):
    ...
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
Django does make one adjustment to the Meta class of an abstract base class: before installing the Meta attribute, it sets abstract=False. This means that children of abstract base classes don't automatically become abstract classes themselves. Of course, you can make an abstract base class that inherits from another abstract base class. You just need to remember to explicitly set abstract=True each time.

Some attributes won't make sense to include in the Meta class of an abstract base class. For example, including db_table would mean that all the child classes (the ones that don't specify their own Meta) would use the same database table, which is almost certainly not what you want.

Be careful with related_name
If you are using the related_name attribute on a ForeignKey or ManyToManyField, you must always specify a unique reverse name for the field. This would normally cause a problem in abstract base classes, since the fields on this class are included into each of the child classes, with exactly the same values for the attributes (including related_name) each time.

Changed in Django 1.2: Please see the release notes
To work around this problem, when you are using related_name in an abstract base class (only), part of the name should contain '%(app_label)s' and '%(class)s'.

'%(class)s' is replaced by the lower-cased name of the child class that the field is used in.
'%(app_label)s' is replaced by the lower-cased name of the app the child class is contained within. Each installed application name must be unique and the model class names within each app must also be unique, therefore the resulting name will end up being different.
For example, given an app common/models.py:

class Base(models.Model):
    m2m = models.ManyToManyField(OtherModel, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True

class ChildA(Base):
    pass

class ChildB(Base):
    pass
Along with another app rare/models.py:

from common.models import Base

class ChildB(Base):
    pass
The reverse name of the common.ChildA.m2m field will be common_childa_related, whilst the reverse name of the common.ChildB.m2m field will be common_childb_related, and finally the reverse name of the rare.ChildB.m2m field will be rare_childb_related. It is up to you how you use the '%(class)s' and '%(app_label)s portion to construct your related name, but if you forget to use it, Django will raise errors when you validate your models (or run syncdb).

If you don't specify a related_name attribute for a field in an abstract base class, the default reverse name will be the name of the child class followed by '_set', just as it normally would be if you'd declared the field directly on the child class. For example, in the above code, if the related_name attribute was omitted, the reverse name for the m2m field would be childa_set in the ChildA case and childb_set for the ChildB field.

Multi-table inheritance
The second type of model inheritance supported by Django is when each model in the hierarchy is a model all by itself. Each model corresponds to its own database table and can be queried and created individually. The inheritance relationship introduces links between the child model and each of its parents (via an automatically-created OneToOneField). For example:

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField()
    serves_pizza = models.BooleanField()
All of the fields of Place will also be available in Restaurant, although the data will reside in a different database table. So these are both possible:

>>> Place.objects.filter(name="Bob's Cafe")
>>> Restaurant.objects.filter(name="Bob's Cafe")
If you have a Place that is also a Restaurant, you can get from the Place object to the Restaurant object by using the lower-case version of the model name:

>>> p = Place.objects.get(id=12)
# If p is a Restaurant object, this will give the child class:
>>> p.restaurant
<Restaurant: ...>
However, if p in the above example was not a Restaurant (it had been created directly as a Place object or was the parent of some other class), referring to p.restaurant would raise a Restaurant.DoesNotExist exception.

Meta and multi-table inheritance
In the multi-table inheritance situation, it doesn't make sense for a child class to inherit from its parent's Meta class. All the Meta options have already been applied to the parent class and applying them again would normally only lead to contradictory behavior (this is in contrast with the abstract base class case, where the base class doesn't exist in its own right).

So a child model does not have access to its parent's Meta class. However, there are a few limited cases where the child inherits behavior from the parent: if the child does not specify an ordering attribute or a get_latest_by attribute, it will inherit these from its parent.

If the parent has an ordering and you don't want the child to have any natural ordering, you can explicitly disable it:

class ChildModel(ParentModel):
    ...
    class Meta:
        # Remove parent's ordering effect
        ordering = []
Inheritance and reverse relations
Because multi-table inheritance uses an implicit OneToOneField to link the child and the parent, it's possible to move from the parent down to the child, as in the above example. However, this uses up the name that is the default related_name value for ForeignKey and ManyToManyField relations. If you are putting those types of relations on a subclass of another model, you must specify the related_name attribute on each such field. If you forget, Django will raise an error when you run validate or syncdb.

For example, using the above Place class again, let's create another subclass with a ManyToManyField:

class Supplier(Place):
    # Must specify related_name on all relations.
    customers = models.ManyToManyField(Restaurant, related_name='provider')
Specifying the parent link field
As mentioned, Django will automatically create a OneToOneField linking your child class back any non-abstract parent models. If you want to control the name of the attribute linking back to the parent, you can create your own OneToOneField and set parent_link=True to indicate that your field is the link back to the parent class.

Proxy models
When using multi-table inheritance, a new database table is created for each subclass of a model. This is usually the desired behavior, since the subclass needs a place to store any additional data fields that are not present on the base class. Sometimes, however, you only want to change the Python behavior of a model -- perhaps to change the default manager, or add a new method.

This is what proxy model inheritance is for: creating a proxy for the original model. You can create, delete and update instances of the proxy model and all the data will be saved as if you were using the original (non-proxied) model. The difference is that you can change things like the default model ordering or the default manager in the proxy, without having to alter the original.

Proxy models are declared like normal models. You tell Django that it's a proxy model by setting the proxy attribute of the Meta class to True.

For example, suppose you want to add a method to the standard User model that will be used in your templates. You can do it like this:

from django.contrib.auth.models import User

class MyUser(User):
    class Meta:
        proxy = True

    def do_something(self):
        ...
The MyUser class operates on the same database table as its parent User class. In particular, any new instances of User will also be accessible through MyUser, and vice-versa:

>>> u = User.objects.create(username="foobar")
>>> MyUser.objects.get(username="foobar")
<MyUser: foobar>
You could also use a proxy model to define a different default ordering on a model. The standard User model has no ordering defined on it (intentionally; sorting is expensive and we don't want to do it all the time when we fetch users). You might want to regularly order by the username attribute when you use the proxy. This is easy:

class OrderedUser(User):
    class Meta:
        ordering = ["username"]
        proxy = True
Now normal User queries will be unordered and OrderedUser queries will be ordered by username.

QuerySets still return the model that was requested
There is no way to have Django return, say, a MyUser object whenever you query for User objects. A queryset for User objects will return those types of objects. The whole point of proxy objects is that code relying on the original User will use those and your own code can use the extensions you included (that no other code is relying on anyway). It is not a way to replace the User (or any other) model everywhere with something of your own creation.

Base class restrictions
A proxy model must inherit from exactly one non-abstract model class. You can't inherit from multiple non-abstract models as the proxy model doesn't provide any connection between the rows in the different database tables. A proxy model can inherit from any number of abstract model classes, providing they do not define any model fields.

Proxy models inherit any Meta options that they don't define from their non-abstract model parent (the model they are proxying for).

Proxy model managers
If you don't specify any model managers on a proxy model, it inherits the managers from its model parents. If you define a manager on the proxy model, it will become the default, although any managers defined on the parent classes will still be available.

Continuing our example from above, you could change the default manager used when you query the User model like this:

class NewManager(models.Manager):
    ...

class MyUser(User):
    objects = NewManager()

    class Meta:
        proxy = True
If you wanted to add a new manager to the Proxy, without replacing the existing default, you can use the techniques described in the custom manager documentation: create a base class containing the new managers and inherit that after the primary base class:

# Create an abstract class for the new manager.
class ExtraManagers(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True

class MyUser(User, ExtraManagers):
    class Meta:
        proxy = True
You probably won't need to do this very often, but, when you do, it's possible.

Differences between proxy inheritance and unmanaged models
Proxy model inheritance might look fairly similar to creating an unmanaged model, using the managed attribute on a model's Meta class. The two alternatives are not quite the same and it's worth considering which one you should use.

One difference is that you can (and, in fact, must unless you want an empty model) specify model fields on models with Meta.managed=False. You could, with careful setting of Meta.db_table create an unmanaged model that shadowed an existing model and add Python methods to it. However, that would be very repetitive and fragile as you need to keep both copies synchronized if you make any changes.

The other difference that is more important for proxy models, is how model managers are handled. Proxy models are intended to behave exactly like the model they are proxying for. So they inherit the parent model's managers, including the default manager. In the normal multi-table model inheritance case, children do not inherit managers from their parents as the custom managers aren't always appropriate when extra fields are involved. The manager documentation has more details about this latter case.

When these two features were implemented, attempts were made to squash them into a single option. It turned out that interactions with inheritance, in general, and managers, in particular, made the API very complicated and potentially difficult to understand and use. It turned out that two options were needed in any case, so the current separation arose.

So, the general rules are:

If you are mirroring an existing model or database table and don't want all the original database table columns, use Meta.managed=False. That option is normally useful for modeling database views and tables not under the control of Django.
If you are wanting to change the Python-only behavior of a model, but keep all the same fields as in the original, use Meta.proxy=True. This sets things up so that the proxy model is an exact copy of the storage structure of the original model when data is saved.
Multiple inheritance
Just as with Python's subclassing, it's possible for a Django model to inherit from multiple parent models. Keep in mind that normal Python name resolution rules apply. The first base class that a particular name (e.g. Meta) appears in will be the one that is used; for example, this means that if multiple parents contain a Meta class, only the first one is going to be used, and all others will be ignored.

Generally, you won't need to inherit from multiple parents. The main use-case where this is useful is for "mix-in" classes: adding a particular extra field or method to every class that inherits the mix-in. Try to keep your inheritance hierarchies as simple and straightforward as possible so that you won't have to struggle to work out where a particular piece of information is coming from.

Field name "hiding" is not permitted
In normal Python class inheritance, it is permissible for a child class to override any attribute from the parent class. In Django, this is not permitted for attributes that are Field instances (at least, not at the moment). If a base class has a field called author, you cannot create another model field called author in any class that inherits from that base class.

Overriding fields in a parent model leads to difficulties in areas such as initializing new instances (specifying which field is being initialized in Model.__init__) and serialization. These are features which normal Python class inheritance doesn't have to deal with in quite the same way, so the difference between Django model inheritance and Python class inheritance isn't arbitrary.

This restriction only applies to attributes which are Field instances. Normal Python attributes can be overridden if you wish. It also only applies to the name of the attribute as Python sees it: if you are manually specifying the database column name, you can have the same column name appearing in both a child and an ancestor model for multi-table inheritance (they are columns in two different database tables).

Django will raise a FieldError if you override any model field in any ancestor model.