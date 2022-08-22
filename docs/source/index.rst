Overview
========

Library to make moment-independent periods in python.
It's designed especially for `Regta Framework <https://github.com/SKY-ALIN/regta>`_,
but with an ability to use it independently.

.. image:: https://img.shields.io/pypi/pyversions/regta-period.svg
   :target: https://github.com/SKY-ALIN/regta-period

.. image:: https://github.com/SKY-ALIN/regta-period/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/SKY-ALIN/regta-period

.. image:: https://github.com/SKY-ALIN/regta-period/actions/workflows/code-quality.yml/badge.svg
   :target: https://github.com/SKY-ALIN/regta-period

.. image:: https://codecov.io/gh/SKY-ALIN/regta-period/branch/main/graph/badge.svg?token=NR7AKLXN5H
   :target: https://codecov.io/gh/SKY-ALIN/regta-period

.. image:: https://badge.fury.io/py/regta-period.svg
   :target: https://pypi.org/project/regta-period/

.. image:: https://img.shields.io/github/license/SKY-ALIN/regta-period.svg
   :target: https://github.com/SKY-ALIN/regta-period/blob/main/LICENSE


Moment-Independence Idea Explanation
------------------------------------

This term in this context means that relying on this approach we can get the time to time
points regardless of the points in which we are.

.. code-block::

            |-----------------|
            t1       t2     moment
    --------|--------|--------|--------> time
                     |--------|


Whereas with the standard intervals like :code:`datetime.timedelta`, we get an unnecessary offset:

.. code-block::

            |-----------------|
            t1       t2     moment
    --------|--------|--------|--------|--------> time
                     |-----------------|


For example, it is important in the context of the job scheduler, because when the
scheduler is redeployed or restarted, you can get an unnecessary time shift or
unnecessary execution of the job.


Math Explanation Of Moment-Independence
---------------------------------------

Regular Offset
^^^^^^^^^^^^^^

Regular offset is the same as python's :code:`timedelta` shift e.g. once per :math:`n_1` days,
:math:`n_2` hours, :math:`n_3` minutes, :math:`n_4` seconds, but with the moment-independence idea.

Essentially, it works as a remainder of the time division from the Unix epoch.
Let :math:`t_{unix}` be the moment of the Unix epoch, a moment that we can get a grip on.
:math:`t` is the current moment. Then, the time since epoch is:

.. math::
   :nowrap:

   \begin{eqnarray}
      \Delta t = t - t_{unix}
   \end{eqnarray}

Let :math:`T` be our regular period. Thus, to calculate time until the next moment we must subtract
from our period the remainder of the division by the period. Final function to calculate
time until the next moment since current looks following:

.. math::
   :nowrap:

   \begin{eqnarray}
      f(t) = T - ( \Delta t \mod T ) = T - ( ( t - t_{unix} ) \mod T )
   \end{eqnarray}


Time Offset
^^^^^^^^^^^

Time offset is stating the exact time e.g. at 9 pm, at 12 am, at 16:30, etc.
It works as a shift of the starting point in the exact time and time zone:

.. math::
   :nowrap:

   \begin{eqnarray}
      t_{unix} + \Delta t_{time} + \Delta t_{tz}
   \end{eqnarray}

Note that it's not possible to combine exact time and short regular intervals such as
hours, minutes, and seconds.


Time Windows
^^^^^^^^^^^^

Time window is a static time frame in which the result should be included e.g. every Monday, every June, etc.
A window may be from :math:`t_{min}` to :math:`t_{max}`, then function result must be included in this interval:

.. math::
   :nowrap:

   \begin{eqnarray}
      t + f(t) \in [t_{min}, t_{max}]
   \end{eqnarray}

If the expression above is true, it means that the result is included in the time window, and the result is correct.
If don't, we calculate the result from the maximum and calculate the next time window until we find a match:

.. math::
   :nowrap:

   \begin{eqnarray}
      t + f(t) \notin [t_{min_n}, t_{max_n}] \longrightarrow f(t_{max_n}); [t_{min_{n+1}}, t_{max_{n+1}}]
   \end{eqnarray}


Installation
------------

Install using :code:`pip install regta-period` or :code:`poetry add regta-period`

If you use python < 3.9, then also install backports: :code:`pip install "backports.zoneinfo[tzdata]"`


Examples
--------

There are two ways to create periods: old school style and hipster style:

.. code-block:: python

    from datetime import datetime
    from zoneinfo import ZoneInfo
    from regta_period import Period

    # Hipster style
    p = Period().every(3).days.at("17:00").by("Europe/Moscow")

    # Old school style
    p = Period(days=3, time="17:00", timezone=ZoneInfo("Europe/Moscow"))

    # <Period: regular_offset=259200.0s, time_offset=61200s, timezone=Europe/Moscow>
    # Every 3 days at 5 pm by Moscow time

    t = datetime.now(tz=ZoneInfo("Europe/Moscow"))
    next_moment = p.get_next(t)  # f(t) + t

You also may combine a few periods to a single object with the same interface:

.. code-block:: python

    from datetime import datetime
    from regta_period import Period, PeriodAggregation, Weekdays

    # Hipster style
    p = Period().on.weekdays.at("18:00") | Period().on.weekends.at("21:00")
    # You also may replace `|` with `.OR` to write shorter and more human-readable code
    p = Period().on.weekdays.at("18:00").OR.on.weekends.at("21:00")

    # Old school style
    p = PeriodAggregation(
        Period(
            weekdays=[Weekdays.MONDAY, Weekdays.TUESDAY, Weekdays.WEDNESDAY, Weekdays.THURSDAY, Weekdays.FRIDAY],
            time="18:00",
        ),
        Period(
            weekdays=[Weekdays.SATURDAY, Weekdays.SUNDAY],
            time="21:00",
        ),
    )

    # All of the above give the same result:
    # <PeriodAggregation: <Period: regular_offset=86400.0s, time_offset=64800s, weekdays=Tuesday,Monday,Thursday,Wednesday,Friday> OR <Period: regular_offset=86400.0s, time_offset=75600s, weekdays=Sunday,Saturday>>
    # At 6 pm on weekdays (Monday-Friday) and at 9 pm on weekends (Saturday-Sunday)

    t = datetime.now()
    timedelta_to_the_next_moment = p.get_interval(t)  # f(t)



.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   self
   api_reference

.. toctree::
   :caption: Development
   :hidden:

   changelog
   license
   GitHub Repository <https://github.com/SKY-ALIN/regta-period>
   PyPI Page <https://pypi.org/project/regta-period/>
