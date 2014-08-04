
NOTICE (2014-08-04)
====================

I finished to write a POC code and ready to write this LINE library, but I have a lot of works to do these days.. so it might take some time to finish this library..

Therefore, I uploaded [poc.py](poc.py) for someone who wants to play with LINE ASAP! Just edit the POC code and enojoy it before I finish this LINE library~

**Read the instruction** of [poc.py](poc.py#L10) be fore you test the code!

> May the LINE be with you...
> 
> by [carpedm20](http://carpedm20.github.io/about/)

*ps. this code was inspired from [here](http://ssut-dev.tumblr.com/post/79956444735/using-line-with-apache-thrift-protocol)*


LINE
====

**Not finished yet... (2014.08.02 ~)**

May the LINE be with you...

    >>> from line import LineClient
    >>> cli = LineClient(YOUR_ID, YOUR_PASSWORD)

Installing
----------

1. using pip: (Not working right now)

    $ pip install line

1. using easy_install: (Not working right now)

    $ easy_install line 

1. using git: (Not working right now)

    $ git clone git://github.com/carpedm20/line.git
    $ cd line
    $ python setup.py install

Using
-----

First, you need to create a `LineClinet` object with YOUR_ID and YOUR_PASSWORD

    >>> from line import LineClient
    >>> li = LineClient(YOUR_ID, YOUR_PASSWORD)


Screenshot
----------

![alt_tag](http://3.bp.blogspot.com/-FX3ONLEKBBY/U9xJD8JkJbI/AAAAAAAAF2Q/1E7VXOkvYAI/s1600/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA+2014-08-02+%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB+10.47.15.png)


License
-------

Source codes are distributed under BSD license.


Author
------

Taehoon Kim / [@carpedm20](http://carpedm20.github.io/about/)
