# regta-period

**Library to make moment-independent periods in python.
It's designed especially for [Regta Framework](https://github.com/SKY-ALIN/regta), 
but with an ability to use it independently.**

[![versions](https://img.shields.io/pypi/pyversions/regta-period.svg)](https://github.com/SKY-ALIN/regta-period)
![Tests](https://github.com/SKY-ALIN/regta-period/actions/workflows/tests.yml/badge.svg)
![Code Quality](https://github.com/SKY-ALIN/regta-period/actions/workflows/code-quality.yml/badge.svg)
[![codecov](https://codecov.io/gh/SKY-ALIN/regta-period/branch/main/graph/badge.svg?token=NR7AKLXN5H)](https://codecov.io/gh/SKY-ALIN/regta-period)
[![PyPI version](https://badge.fury.io/py/regta-period.svg)](https://pypi.org/project/regta-period/)
[![license](https://img.shields.io/github/license/SKY-ALIN/regta-period.svg)](https://github.com/SKY-ALIN/regta-period/blob/main/LICENSE)

## Moment-Independence Idea Explanation

This term in this context means that relying on this approach we can get the time to time 
points regardless of the points in which we are.
```
        |-----------------|
        t1       t2     moment
--------|--------|--------|--------> time
                 |--------|
```

Whereas with the standard intervals like `datetime.timedelta`, we get an unnecessary offset:
```
        |-----------------|
        t1       t2     moment
--------|--------|--------|--------|--------> time
                 |-----------------|
```

For example, it is important in the context of the job scheduler, because when the
scheduler is redeployed or restarted, you can get an unnecessary time shift or
unnecessary execution of the job.

## Math Explanation Of Moment-Independence

### Regular Offset

Regular offset is the same as python's `timedelta` shift e.g. once per $n_1$ days,
$n_2$ hours, $n_3$ minutes, $n_4$ seconds, but with the moment-independence idea.

Essentially, it works as a remainder of the time division from the Unix epoch.
Let $t_{unix}$ be the moment of the Unix epoch, a moment that we can get a grip on.
$t$ is the current moment. Then, the time since epoch is:

$$\ \Delta t = t - t_{unix} $$

Let $T$ be our regular period. Thus, to calculate time until the next moment we must subtract
from our period the remainder of the division by the period. Final function to calculate
time until the next moment since current looks following:

$$\ f(t) = T - ( \Delta t \mod T ) = T - ( ( t - t_{unix} ) \mod T ) $$

### Time Offset

Time offset is stating the exact time e.g. at 9 pm, at 12 am, at 16:30, etc.
It works as a shift of the starting point in the exact time and time zone:

$$\ t_{unix} + \Delta t_{time} + \Delta t_{tz} $$

Note that it's not possible to combine exact time and short regular intervals such as
hours, minutes, and seconds.

### Time Windows

Time window is a static time frame in which the result should be included e.g. every Monday, every June, etc. 
A window may be from $t_{min}$ to $t_{max}$, then function result must be included in this interval:

$$ t + f(t) \in [t_{min}, t_{max}] $$

If the expression above is true, it means that the result is included in the time window, and the result is correct. 
If don't, we calculate the result from the maximum and calculate the next time window until we find a match:

$$ t + f(t) \notin [t_{min_n}, t_{max_n}] \longrightarrow f(t_{max_n}); [t_{min_{n+1}}, t_{max_{n+1}}] $$

## Installation

Install using `pip install regta-period` or `poetry add regta-period`

If you use python < 3.9, then also install backports: `pip install "backports.zoneinfo[tzdata]"`

## Examples

There are two ways to create periods: old school style and hipster style.

```python
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
next_moment: datetime = p.get_next(t)  # f(t) + t
```

You also may combine a few periods to a single object with the same interface:

```python
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

# All of the above will the same result:
# <PeriodAggregation: <Period: regular_offset=86400.0s, time_offset=64800s, weekdays=Tuesday,Monday,Thursday,Wednesday,Friday> OR <Period: regular_offset=86400.0s, time_offset=75600s, weekdays=Sunday,Saturday>>
# At 6 pm on weekdays (Monday-Friday) and at 9 pm on weekends (Saturday-Sunday)

t = datetime.now()
timedelta_to_the_next_moment = p.get_interval(t)  # f(t)
```

---

Full documentation and reference are available at 
[regta-period.alinsky.tech](https://regta-period.alinsky.tech)
